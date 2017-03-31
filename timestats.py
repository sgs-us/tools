#!env python3

import argparse, logging, subprocess, sys, threading, time
import numpy as np

log = logging.getLogger(sys.argv[0])

def setup_argparse():
    parser = argparse.ArgumentParser(description='Times processes.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--rep", "-r", default=1, type=int, help='Number of repetitions')
    parser.add_argument("--time", "-t", default=0, type=float, help='Maximum total runtime of timing tests')
    parser.add_argument("--timestamps", "-s", help="Print regular timestamps to stdout.")
    parser.add_argument("--verbose", "-v", action="store_const", const=0, default=15, help='Generate more output')
    parser.add_argument("command", help="Command to execute", nargs=argparse.REMAINDER)
    return parser

def setup_logging(level):
    # CRITICAL	50
    # ERROR	40
    # WARNING	30
    # INFO	20
    # DEBUG	10
    # NOTSET	0
    logging.basicConfig(level=level,
                        format = "%(levelname)s: %(message)s")


def execute(cmd):
    log.debug("Executing command: %s", cmd)
    t0 = time.time()
    ret_code = subprocess.call(cmd, shell = True)
    t1 = time.time()
    log.info("Executing command took {:5.4} seconds.".format(t1 - t0))
    if ret_code != 0:
        log.warning("'%s' returned with %s", cmd, ret_code)
    return t1 - t0

def measure(cmd, max_time, max_rep):
    exec_counter = 0
    max_time = max_time if max_time else sys.maxsize
    times = []

    t0 = time.time()
    while(True):
        exec_counter += 1
        log.debug("Repetition {} of {}, time elapsed {:.4} of max {}".format(exec_counter, max_rep,  time.time() - t0, max_time))
        times.append(execute(cmd))
        if exec_counter >= max_rep:
            log.info("Maximum number of %s repetitions reached.", max_rep)
            break
        if time.time() - t0 > max_time:
            log.info("Maximum execution time of %s seconds reached.", max_time)
            break

    total_time =  time.time() - t0
    return times        
        
def parse_timestamps(timestamps):
    return float(timestamps)


def start_timestamping(interval):
    t0 = time.time()

    i = 0
    while True:
        i += 1
        time.sleep(interval)
        log.info("==== Timestamp {}, time elapsed {:.4}s ====".format(i, time.time() - t0))

    
def main():
    parser = setup_argparse()
    args = parser.parse_args()
    setup_logging(args.verbose)
    command = " ".join(args.command) # concatenate the remaining arguments.
    if args.timestamps:
        interval = parse_timestamps(args.timestamps)
        thread = threading.Thread( target = start_timestamping, name="Timestamping", args = (interval, ) )
        thread.daemon = True
        log.debug("Start timestamping thread with interval %s.", interval)
        thread.start()
                
    times = measure(command, args.time, args.rep)
    times = np.sort(times)
    log.info("Execution of %s finished." % command)
    log.info("Total time: {:.4} seconds for {} runs.".format(np.sum(times), len(times)))
    log.info("Max: {:.4}, Min: {:.4}, Mean: {:.4}, StdDev: {:.6f}".format(np.max(times), np.min(times), np.mean(times), np.std(times)))
    if len(times) > 2:
        log.info("More than 2 runs, printing results without the slowest and fastest run: ")
        t = times[1:-1]
        log.info("  Total time: {:.4} seconds for {} runs.".format(np.sum(t), len(t)))
        log.info("  Max: {:.4}, Min: {:.4}, Mean: {:.4}, StdDev: {:.6f}".format(np.max(t), np.min(t), np.mean(t), np.std(t)))
    
    log.debug(times)

if __name__ == "__main__":
    main()

