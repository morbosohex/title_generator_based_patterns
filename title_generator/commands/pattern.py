import click
from title_generator.commands.base import cli

from title_generator.kw_generator.Config import Config
from title_generator.pattern_generator import pattern_for_label_num
from title_generator.pattern_generator import get_labels
from title_generator.pattern_generator import combinations_patterns
from title_generator.pattern_generator import dump_patterns
config = Config()
__author__ = 'lin'


@cli.command(help="Generate patterns from given certain hyperparameter")
@click.option('--init-label-num', '-i',
              type=click.IntRange(1, 10),
              default=4,
              help="number of labels in each pattern of no-duplicated label")
@click.option('--must_include_label', '-m',
              multiple=True,
              default=['product', 'other'],
              help="label must contained in each unique pattern")
@click.option('--min_words_num', '-l',
              type=click.IntRange(1, 10),
              default=3,
              help="expand pattern setup, minimum words in each pattern")
@click.option('--max_words_num', '-h',
              type=click.IntRange(1, 10),
              default=10,
              help="expand pattern setup, maximum words in each pattern")
@click.option('--max_num_unique_label', '-u',
              type=click.IntRange(1, 10),
              default=3,
              help="maximum unique labels in each pattern")
@click.option('--priority_limit', '-p',
              type=click.IntRange(5, 50),
              default=10,
              help="lowest priority of each pattern, `1` means highest")
@click.option('--output', '-o', default='patterns.csv',
              help="patterns file to output (default = './patterns.csv')")
@click.pass_context
def pattern(ctx, init_label_num, must_include_label,
            min_words_num, max_words_num, max_num_unique_label,
            priority_limit, output):
    click.echo("\nGet Labels Category...")
    labels = get_labels(config)
    patterns = pattern_for_label_num(labels, init_label_num,
                                     *must_include_label)
    click.echo("\nRunning 'pattern' command with:")

    kwargs = config.kw_threshold

    total_patterns = combinations_patterns(patterns,
                                           min_words_num,
                                           max_words_num,
                                           max_num_unique_label,
                                           priority_limit,
                                           **kwargs)
    dump_patterns(total_patterns, output)
    click.echo("\nPatterns Generate Completely!")


