import socket
import struct
import hashlib
from typing import Optional, Tuple

class SymveaClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 24096):
        self.host = host
        self.port = port
        self.socket = None
    
    def connect(self):
        """Connect to Symvea server"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self._handshake()
    
    def _handshake(self):
        """Perform handshake with server"""
        # Send handshake
        handshake = b"SYMVEA\x01\x00"
        self.socket.send(handshake)
        
        # Read response
        response = self.socket.recv(8)
        if response != b"SYMVEA\x01\x00":
            raise Exception("Handshake failed")
    
    def upload(self, key: str, data: bytes, user_id: Optional[str] = None) -> Tuple[int, int]:
        """Upload data to server"""
        # Frame format: type(1) + key_len(4) + key + data_len(4) + data + user_id_len(4) + user_id
        frame = bytearray()
        frame.append(1)  # Upload frame type
        
        key_bytes = key.encode('utf-8')
        frame.extend(struct.pack('<I', len(key_bytes)))
        frame.extend(key_bytes)
        
        frame.extend(struct.pack('<I', len(data)))
        frame.extend(data)
        
        user_id_bytes = user_id.encode('utf-8') if user_id else b''
        frame.extend(struct.pack('<I', len(user_id_bytes)))
        frame.extend(user_id_bytes)
        
        self.socket.send(frame)
        
        # Read acknowledgment
        response = self._read_frame()
        if response[0] == 2:  # Ack frame
            original_size = struct.unpack('<I', response[1:5])[0]
            compressed_size = struct.unpack('<I', response[5:9])[0]
            return original_size, compressed_size
        else:
            raise Exception("Upload failed")
    
    def download(self, key: str) -> bytes:
        """Download data from server"""
        frame = bytearray()
        frame.append(3)  # Download frame type
        
        key_bytes = key.encode('utf-8')
        frame.extend(struct.pack('<I', len(key_bytes)))
        frame.extend(key_bytes)
        
        self.socket.send(frame)
        
        # Read response
        response = self._read_frame()
        if response[0] == 4:  # Data frame
            data_len = struct.unpack('<I', response[1:5])[0]
            return response[5:5+data_len]
        elif response[0] == 5:  # NotFound frame
            raise FileNotFoundError(f"Key not found: {key}")
        else:
            raise Exception("Download failed")
    
    def verify(self, key: str) -> bool:
        """Verify file integrity"""
        frame = bytearray()
        frame.append(6)  # Verify frame type
        
        key_bytes = key.encode('utf-8')
        frame.extend(struct.pack('<I', len(key_bytes)))
        frame.extend(key_bytes)
        
        self.socket.send(frame)
        
        # Read response
        response = self._read_frame()
        if response[0] == 7:  # Verified frame
            return response[1] == 1  # hash_match boolean
        else:
            raise Exception("Verify failed")
    
    def _read_frame(self) -> bytes:
        """Read a frame from the socket"""
        # Read frame length first
        length_bytes = self.socket.recv(4)
        if len(length_bytes) != 4:
            raise Exception("Connection closed")
        
        frame_length = struct.unpack('<I', length_bytes)[0]
        
        # Read the frame data
        frame_data = b''
        while len(frame_data) < frame_length:
            chunk = self.socket.recv(frame_length - len(frame_data))
            if not chunk:
                raise Exception("Connection closed")
            frame_data += chunk
        
        return frame_data
    
    def close(self):
        """Close connection"""
        if self.socket:
            # Send close frame
            frame = bytearray([0])  # Close frame type
            self.socket.send(frame)
            self.socket.close()
            self.socket = None