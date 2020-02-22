#!/usr/bin/env python3

import argparse
import json
import logging

def pair(s):
    try:
        x, y = map(float, s.split(','))
        return [x, y]
    except:
        raise argparse.ArgumentTypeError("Pairs must be x,y")

def _do_parse_cmdline():
    parser = argparse.ArgumentParser(description='Dynamic GPIO-based fan control for Raspberry Pi.')
    parser.add_argument(
        'curve', 
        nargs='*',
        type=pair,
        default=[
            [0, 0],
            [40, 0],
            [50, 0],
            [60, 0.5],
            [70, 1],
            [80, 1]
        ],
        help='Curve Keypoints; see documentation for long-form details')
    parser.add_argument(
        '--config', '-c',
        type=argparse.FileType('r'),
        default=None,
        help='Configuration file; command line arguments receive priority')
    parser.add_argument(
        '--pin', '-p',
        type=int,
        default=18,
        help='Which GPIO pin to use for PWM signaling')
    parser.add_argument(
        '--frequency', '--freq',  '-f',
        type=int,
        default=20,
        help='PWM frequency')
    parser.add_argument(
        '--pollrate', '-r',
        type=int,
        default=1,
        help='Polling rate in polls / sec')
    parser.add_argument(
        '--loglevel', '-l',
        type=str,
        default='INFO',
        help='Log level; uses Python logging levels')
    parser.add_argument(
        '--logfile', '-o',
        type=argparse.FileType('w', encoding='UTF-8'),
        default='-',
        help='Log file to write to; defaults to stdout')
    return parser.parse_args()

def get_config():
    logformat = "%(levelname)s: %(message)s"
    dateformat = "%Y-%m-%d %H:%M:%S"
    args = _do_parse_cmdline()
    if args.config is not None:
        d = json.load(args.config)
        for key, value in d.items():
            args[key] = value
    logging.basicConfig(
        level=args.loglevel, 
        stream=args.logfile,
        format=logformat,
        datefmt=dateformat)
    args.curve = sorted(args.curve, key=lambda k: k[0], reverse=True)
    return args
