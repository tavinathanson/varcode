# Copyright (c) 2016-2019. Mount Sinai School of Medicine
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import division, absolute_import
import logging
import logging.config
import pkg_resources
import sys

from .version_info import print_version_info
from .variant_args import make_variants_parser, variant_collection_from_args


logging.config.fileConfig(pkg_resources.resource_filename(__name__, 'logging.conf'))
logger = logging.getLogger(__name__)


def main(args_list=None):
    """
    Script which loads variants and annotates them with overlapping genes
    and predicted coding effects.

    Example usage:
        varcode
            --vcf mutect.vcf \
            --vcf strelka.vcf \
            --maf tcga_brca.maf \
            --variant chr1 498584 C G \
            --json-variants more_variants.json
    """
    print_version_info()
    if args_list is None:
        args_list = sys.argv[1:]
    arg_parser = make_variants_parser(
        description="Annotate variants with overlapping gene names and predicted coding effects")
    arg_parser.add_argument("--output-csv", help="Output path to CSV")
    args = arg_parser.parse_args(args_list)
    variants = variant_collection_from_args(args)
    effects = variants.effects()
    effects_dataframe = effects.to_dataframe()
    logger.info('\n%s', effects)
    if args.output_csv:
        effects_dataframe.to_csv(args.output_csv, index=False)
