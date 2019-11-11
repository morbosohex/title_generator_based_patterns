import click
from pprint import pprint
from title_generator.commands.base import cli, set_parameter_value

from title_generator.kw_generator import generate_combinations
from title_generator.kw_generator import generate_combinations_v2
from title_generator.kw_generator import save_combinations
from title_generator.kw_generator import load_dictionary
from title_generator.kw_generator.Config import Config
config = Config()
__author__ = 'lin'


@cli.command(help="Generate keywords from an input directory")
@click.argument('input-dir', type=click.Path(exists=True), default=".")
@click.option('--text/--file', default=True)
@click.option('--verbose', default=False)
@click.option('--keywords', '-k',
              multiple=True,
              default=['apple', 'laptop', 'MacBook Air', 'Retina',
                       'siver', 'gray', '15 inch', '16Gb'])
@click.option('--patterns-file', '-t', default="patterns.csv")
@click.option('--output', '-o', default='titles.csv',
              help="file to output (default = 'titles.csv')")
# @click.help_option()
@click.pass_context
def generate(ctx, input_dir, text, verbose, keywords, patterns_file, output):

    set_parameter_value(ctx, "gen-kw-file", output)

    if text:
        click.echo("Loading dictionary...")
        kw_clf = load_dictionary(config)

        click.echo("\nClassify Keywords...")
        pprint(f">>> {keywords}")
        click.echo("Classify Result...\n>>> ")
        label_keywords = kw_clf.classifier(keywords)
        pprint(list(label_keywords))

        click.echo("\nRunning 'generate' command with:")
        click.echo("ouput_file = " + output)
        # click.echo ("input_dir = " + input_dir)
        combinations = generate_combinations_v2(label_keywords,
                                                patterns_file,
                                                verbose)
    else:
        click.echo("\ninput_dir = " + input_dir)
        combinations = generate_combinations(input_dir,
                                             patterns_file,
                                             verbose)
    click.echo("\nWriting file '%s'" % output)
    save_combinations(output, combinations)
