import pandas as pd
import sys, getopt
from collections import defaultdict

# populate this dictionary with MPN:LCSC_PNs pairs.
# If a component is not found in this dictionary, a null
# string is returned (due to the dictionary being a defaultdict).
LCSC_crossreference_dict = defaultdict(str,{
'CC0805ZKY5V6BB106':'C15850', #CAP CER 10UF 10V Y5V 0805
'CC0603KRX7R7BB104':'C14663', #CAP CER 0.1UF 16V X7R 0603
'SN74AHCT125DR':'C155176', #SN74AHCT125DR
})


class Main():
    def main(self, argv):
        bominputfile = None
        bomoutputfile = None
        pickplacein = None
        pickplaceout = None

        def usage(prog):
            print('{} [-b <upverter bom> -B <JCLPCB bom>] [-p <upverter pickandplace> -P <JCLPCB pickandplace>]'.format(prog))

        try:
            opts, args = getopt.getopt(argv[1:], "hb:B:p:P:")
        except getopt.GetoptError:
            usage(f"{argv[0]}")
            sys.exit(1)

        for opt, arg in opts:
            if opt == '-h':
                usage(f"{argv[0]}")
                sys.exit(2)
            elif opt == '-b':
                bominputfile = arg
            elif opt == '-B':
                bomoutputfile = arg
            elif opt == '-p':
                pickplacein = arg
            elif opt == '-P':
                pickplaceout = arg


        print('Output file is "{}"'.format(bomoutputfile))

        # process the BOM if specified
        if bominputfile and bomoutputfile:
            # import only the columns we need.
            df = pd.read_csv(bominputfile, usecols=['Description', 'Reference Designator','Mfg Package Ident', 'Manufacturer Part Number'  ])

            # crossreference to LCSC PNs
            df['Manufacturer Part Number'] = df['Manufacturer Part Number'].map(LCSC_crossreference_dict)

            # remap headers to JCLPCB names
            df.rename(columns={
                'Reference Designator': 'Designator',
                'Mfg Package Ident': 'Footprint',
                'Manufacturer Part Number': 'LCSC Part #（optional）',
                'Description': 'Comment'}, inplace = True)

            # write out the new bom
            df.to_csv(bomoutputfile, index = False, header=True)

        # process the pick and place file if specified
        if pickplacein and pickplaceout:
            # read only the columns we care about.
            df = pd.read_csv(pickplacein, usecols=['Part', 'X','Y', 'Rotation'])

            # remap headers to JCLPCB names
            df.rename(columns={
                'Part': 'Designator',
                'X': 'Mid X',
                'Y': 'Mid Y',
                #'Rotation': 'Rotation'}, # no need to remap
                }, inplace = True)
            # add the 'Layer' column and mark everything as on the Top.
            df['Layer']='Top' # default all parts to the top side

            # convert MILs to mm
            for cn in ['Mid X', 'Mid Y']:
                df[cn] = df[cn] * 25.4 / 1000.

            # write out the new pick and place file
            df.to_csv(pickplaceout, index = False, header=True)

if __name__ == "__main__":
    Main().main(sys.argv)
    sys.exit(0)
