from tqdm import tqdm
import logging
import json
from pathlib import Path
from flowmapper.cas import CAS
from flowmapper.match import match_rules
from flowmapper.flow import Flow
from scripts.utils import field_mapping, read_flowlist

logger = logging.getLogger(__name__)

def main(source_filepath: Path, target_filepath: Path, fields, output_file: Path = Path('mapping.json')):
    fields = field_mapping(fields)
    source_flows = [Flow.from_dict(flow, fields['source']) for flow in read_flowlist(source_filepath)]
    target_flows = [Flow.from_dict(flow, fields['target']) for flow in read_flowlist(target_filepath)]

    rules = match_rules()
    mappings = []
    for source_flow in tqdm(source_flows):
        for target_flow in target_flows:
            for rule in rules:
                is_match = rule(source_flow, target_flow, fields)
                if is_match:
                    mappings.append(is_match)
                    break

    with open(output_file, 'w') as fs:
        json.dump(mappings, fs, indent=2)
