'''
Parse an SraRunTable.txt as provided by the sequence read archive
into a the basic config.yaml structure for 'runs', 'samples' and
'sample_annotations'. This will have to be manually pasted into a
foncig yaml, as grouping of samples and pipeline configuration are
usually unique to an analysis. The run table should be the first
command line argument.
'''

import csv
import sys
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


def amplification( sample ):
    '''
    Determine whether the library is amplified and if so with which method.
    '''
    if ( sample == 'RC-T' ) | ( sample == 'RN-T' ):
        return "none"
    else:
        cell = sample.split(sep = '-')[0]
        if ( cell == "RC" ) | ( cell == "RN" ):
            return "MDA"
        else:
            sys.exit("Encountered unknown sample name: '{}'. Please implement amplification handling before using this script's output.\n", sn)


def selection( sample ):
    '''
    Determine whether the library underwent some sort of target selection.
    '''
    if ( sample == 'RC-T' ) | ( sample == 'RN-T' ):
        return "WX"
    else:
        cell = sample.split(sep = '-')[0]
        if ( cell == "RC" ) | ( cell == "RN" ):
            return "WX"
        else:
            sys.exit("Encountered unknown sample name: '{}'. Please implement library selection handling before using this script's output.\n", sn)


def batch_key( sample ):
    '''
    Create a unique batch key for each run, to sensibly group runs.
    '''
    if sample == 'RC-T':
        return "ccRCC_tumor_bulk"
    elif sample == 'RN-T':
        return "ccRCC_normal_bulk"
    else:
        cell = sample.split(sep = '-')[0]
        if cell == "RC":
            return "ccRCC_tumor_single-cell"
        elif cell == "RN":
            return "ccRCC_normal_single-cell"
        else:
            sys.exit("Encountered unknown sample name: '{}'. Please implement batch handling before using this script's output.\n", sn)

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
            sample_name = row['Sample_Name_s'].split(sep = '_')[1]
            out_dict['runs'][ run ] = paired_vs_single( row['LibraryLayout_s'] )
            out_dict['samples'].setdefault( sample_name, []).append( run )
            
            if sample_name not in out_dict['batches'].setdefault( batch_key( sample_name ), []):
                out_dict['batches'][ batch_key( sample_name ) ].append( sample_name )
            out_dict['sample_annotations'][ sample_name ] = {
                'amplification': amplification( sample_name ),
                'library_selection': selection( sample_name ),
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

