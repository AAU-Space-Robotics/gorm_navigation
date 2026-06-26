import numpy as np


def yaw_quat(quat: np.ndarray) -> np.ndarray:
    """
    Extract yaw component from a quaternion and return a new quaternion 
    representing only rotation around the yaw axis.
    
    Args:
        quat: Quaternion in [w, x, y, z] format
        
    Returns:
        Normalized quaternion representing yaw-only rotation
    """
    qw, qx, qy, qz = quat  # Unpack quaternion components

    # Calculate yaw
    yaw = np.arctan2(2.0 * (qw * qz + qx * qy), 1.0 - 2.0 * (qy**2 + qz**2))

    # Create a new quaternion representing rotation around the yaw axis
    quat_yaw = np.array([np.cos(yaw / 2), 0.0, 0.0, np.sin(yaw / 2)])

    # Normalize the resulting quaternion
    norm = np.linalg.norm(quat_yaw)
    if norm == 0:
        return quat_yaw  # Return as is if norm is zero to avoid division by zero
    quat_yaw /= norm

    return quat_yaw


def quat_rotate_inverse(quat: np.ndarray, vec: np.ndarray) -> np.ndarray:
    """
    Rotate a vector by the inverse of a quaternion.
    This effectively transforms a vector from world frame to the frame 
    represented by the quaternion.
    
    Args:
        quat: Quaternion in [w, x, y, z] format
        vec: 3D vector to rotate
        
    Returns:
        Rotated vector
    """
    q_w = quat[0]  # Scalar part of quaternion
    q_vec = quat[1:]  # Vector part of quaternion

    # Component A: Scalar calculation and multiplication with vec
    a = vec * (2.0 * q_w**2 - 1.0)

    # Component B: Cross product scaled by quaternion scalar part
    b = np.cross(q_vec, vec) * q_w * 2.0

    # Component C: Dot product for scaling q_vec
    c = q_vec * np.dot(q_vec, vec) * 2.0

    # Combine components
    return a - b + c


def quaternion_to_euler(x: float, y: float, z: float, w: float) -> tuple:
    """
    Convert a quaternion into euler angles (yaw, pitch, roll).
    
    Args:
        x, y, z, w: Quaternion components
        
    Returns:
        Tuple of (yaw, pitch, roll) in radians
    """
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = np.arctan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = np.arcsin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = np.arctan2(t3, t4)

    return yaw_z, pitch_y, roll_x
