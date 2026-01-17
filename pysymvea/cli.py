#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from .client import SymveaClient

def main():
    parser = argparse.ArgumentParser(description='Symvea Python client')
    parser.add_argument('--host', default='127.0.0.1:24096', help='Server host:port')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Upload command
    upload_parser = subparsers.add_parser('upload', help='Upload file')
    upload_parser.add_argument('file', help='File to upload')
    upload_parser.add_argument('--user-id', help='User ID')
    
    # Download command
    download_parser = subparsers.add_parser('download', help='Download file')
    download_parser.add_argument('key', help='Key to download')
    download_parser.add_argument('-o', '--output', help='Output file')
    
    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify file')
    verify_parser.add_argument('key', help='Key to verify')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Parse host:port
    if ':' in args.host:
        host, port = args.host.split(':')
        port = int(port)
    else:
        host = args.host
        port = 24096
    
    client = SymveaClient(host, port)
    
    try:
        client.connect()
        
        if args.command == 'upload':
            file_path = Path(args.file)
            if not file_path.exists():
                print(f"❌ File not found: {args.file}")
                return 1
            
            data = file_path.read_bytes()
            key = file_path.name
            
            original_size, compressed_size = client.upload(key, data, args.user_id)
            compression_ratio = ((original_size - compressed_size) / original_size) * 100
            
            print("✅ Upload successful!")
            print(f"   Key: {key}")
            print(f"   Original: {original_size} bytes")
            print(f"   Compressed: {compressed_size} bytes")
            print(f"   Compression: {compression_ratio:.1f}%")
        
        elif args.command == 'download':
            try:
                data = client.download(args.key)
                output_file = args.output or args.key
                
                Path(output_file).write_bytes(data)
                print("✅ Download successful!")
                print(f"   Size: {len(data)} bytes")
                print(f"   Saved to: {output_file}")
            except FileNotFoundError as e:
                print(f"❌ {e}")
                return 1
        
        elif args.command == 'verify':
            try:
                is_valid = client.verify(args.key)
                if is_valid:
                    print("✅ VERIFIED - File integrity confirmed")
                else:
                    print("❌ CORRUPTION DETECTED - File integrity check failed")
            except Exception as e:
                print(f"❌ Verification failed: {e}")
                return 1
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    finally:
        client.close()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())