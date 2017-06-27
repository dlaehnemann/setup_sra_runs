'''
Parse an SraRunTable.txt as provided by the sequence read archive
into a the basic config.yaml structure for 'runs', 'samples' and
'sample_annotations'. This will have to be manually pasted into a
foncig yaml, as grouping of samples and pipeline configuration are
usually unique to an analysis. The run table should be the first
command line argument.
'''

import csv, sys
import yaml

def paired_vs_single(library_layout):
    '''
    Determine whether the library is paired-end or single end.
    '''
    if library_layout == 'PAIRED':
        return 'pair'
    elif library_layout == 'SINGLE':
        return 'single'
    else:
        sys.exit("Encountered unknown library layout: '{}'. Please implement handling before using this script's output.\n", library_layout)


def amplification(assay):
    '''
    Determine whether the library is amplified and if so with which method.
    '''
    if assay == 'MDA':
        return 'MDA'
    elif assay == 'WGA':
        sys.stderr.write("Undetermined whole genome amplification method '%s', defaults to 'MDA'. Please make sure this default is correct for your data.\n" % assay)
        return 'MDA'
    elif assay == 'AMPLICON':
        return 'AMPLICON'
    elif assay == 'WXS':
        return 'none'
    else:
        sys.exit("Encountered unknown assay type: '{}'. Please implement handling before using this script's output.\n", assay)


def selection(assay, selection):
    '''
    Determine whether the library underwent some sort of target selection.
    '''
    if ( assay == 'WXS' ) & ( selection == 'Hybrid Selection' ):
        return 'WX'
    elif ( assay == 'WGA' ) & ( selection == 'PCR' ):
        return 'AMPLICON'
    elif ( assay == 'AMPLICON' ) & ( selection == 'PCR' ):
        return 'AMPLICON'
    else:
        sys.exit("Encountered unknown assay type: '{}'. Please implement handling before using this script's output.\n", assay)


def batch_key( sn, amp ):
    '''
    Create a unique batch key for each run, to sensibly group runs.
    '''
    patient = sn.split(sep = '_')[0]
    if amp == 'none':
        return patient + "_bulk"
    elif amp == 'AMPLICON':
        return patient + "_amplicon"
    elif amp == 'MDA':
        return patient + "_cells"
    else:
        sys.exit("Encountered unknown amplification type: '{}'. Please implement handling before using this script's output.\n", amplif)

out_dict = {}
out_dict['runs'] = {}
out_dict['samples'] = {}
out_dict['batches'] = {}
out_dict['sample_annotations'] = {}

in_file = 'SraRunTable.txt'
with open(in_file, newline='') as t:
    reader = csv.DictReader(t, delimiter='\t')
    try:
        for row in reader:
            run = row['Run_s']
            assay = row['Assay_Type_s']
            sample_name = row['Sample_Name_s']
            out_dict['runs'][ run ] = paired_vs_single( row['LibraryLayout_s'] )
            out_dict['samples'][ run ] = [ run ]
            amplif = amplification( assay )
            key = batch_key( sample_name, amplif )
            out_dict['batches'].setdefault(key, []).append( run )
            out_dict['sample_annotations'][ run ] = {
                'amplification': amplif,
                'library_selection': selection( assay, row['LibrarySelection_s'] ),
                'library_source': row['LibrarySource_s'],
                'machine': row['Instrument_s'],
                'platform': row['Platform_s']
            }
    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(in_file, reader.line_num, e))

out_file = open('runs.yaml', "w")
try:
    out_file.write( yaml.dump(out_dict, default_flow_style=False) )
except yaml.Error as e:
    sys.exit('file {}: {}'.format(out_file, e))

