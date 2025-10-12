from argparse import Namespace, ArgumentParser
import logging
import os
from pathlib import Path
import sys

from mock_wx.test_runner import Tester, Actions

def main(cmdline: Namespace) -> int:
    os.environ["CALL_DIFF_RUNNER"] = ""
    sys.path.append(str(cmdline.base_dir))
    tester = Tester(cmdline)
    logging.basicConfig(level=getattr(logging, args.log_level), stream=tester.log)
    return_code = tester.run()
    tester.write((Actions.EXIT, return_code))
    return return_code


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("base_dir", type=Path, help="Base directory of all unit tests")
    parser.add_argument("tests", nargs="*", help="Tests to run")
    parser.add_argument("-n", "--no-run", help="Scan only, don't run tests", action="store_true")
    parser.add_argument("-l", "--log-level", help="Set the logging level", default="WARNING")
    parser.add_argument("-s", "--start-at", help="Start running all tests starting with this one", action="store_true")
    args = parser.parse_args()
    # args = Namespace(base_dir=Path(r"C:\git\CallDiff\scratch"), log_level="DEBUG")
    sys.exit(main(args))
