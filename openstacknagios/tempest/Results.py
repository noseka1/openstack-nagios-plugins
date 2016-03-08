#
#    Copyright (C) 2016 Ales Nosek <ales.nosek@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
  Nagios/Icinga plugin to check Tempest results.

  Takes the output of 'rally verify results --json' as input on stdin.
  and checks the number of test failures, successes and the test duration.

"""

import openstacknagios.openstacknagios as osnag
import sys
import json

class TempestResults(osnag.Resource):
    """
    """

    def __init__(self, args=None):
        if args.resultfile:
            infile = open(args.resultfile, 'r')

            with infile:
                try:
                    self.results=json.load(infile)
                except ValueError:
                    raise SystemExit(sys.exc_info()[1])
        else:
            self.results=json.load(sys.stdin)

        osnag.Resource.__init__(self)

    def probe(self):

        success = self.results['success']
        failures = self.results['failures']
        time = float(self.results['time'])

        yield osnag.Metric('success', success)
        yield osnag.Metric('failures', failures )
        yield osnag.Metric('duration', time, uom='s' )

@osnag.guarded
def main():
    argp = osnag.ArgumentParser(description=__doc__)

    argp.add_argument('--resultfile',
                      help='file to read results from (output of rally task results) if not specified, stdin is used.' )

    argp.add_argument('-w', '--warn', metavar='RANGE', default=':0',
                      help='return warning if failure counter is outside RANGE (default: :0, warn if any failures)')
    argp.add_argument('-c', '--critical', metavar='RANGE', default=':0',
                      help='return critical if failure counter is outside RANGE (default :0, critical if any failures)')

    argp.add_argument('--warn_success', metavar='RANGE', default='0:',
                      help='return warning if success counter is outside RANGE (default: 0:, never warn)')
    argp.add_argument('--critical_success', metavar='RANGE', default='0:',
                      help='return critical if success counter is outside RANGE (default: 0:, never critical)')

    argp.add_argument('--warn_duration', metavar='RANGE', default='0:',
                      help='return warning if test duration is outside RANGE (default: 0:, never warn)')
    argp.add_argument('--critical_duration', metavar='RANGE', default='0:',
                      help='return critical if test duration is outside RANGE (default: 0:, never critical)')

    args = argp.parse_args()

    check = osnag.Check(
        TempestResults(args=args),
        osnag.ScalarContext('failures', args.warn, args.critical),
        osnag.ScalarContext('success', args.warn_success, args.critical_success),
        osnag.ScalarContext('duration', args.warn_duration, args.critical_duration),
        osnag.Summary(show=['failures','duration'])
        )
    check.main(verbose=args.verbose, timeout=args.timeout)

if __name__ == '__main__':
    main()
