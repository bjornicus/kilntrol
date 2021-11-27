import argparse

def create_arg_parser():
    parser = argparse.ArgumentParser(description='Control your Kiln')
    parser.add_argument('--profile', '-p', required=True, type=argparse.FileType('r') ,help='the profile to run')
    parser.add_argument('--time', '-t', default="00:00:00", help='time offset within the profile to start at.')
    parser.add_argument('--simulate', action='store_true', help='use a simulated kiln instead of real hardware')
    return parser
