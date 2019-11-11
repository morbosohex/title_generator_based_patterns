from title_generator import csv
from title_generator.commands.base import cli
from title_generator.commands.base import get_awr_cloud_project
from title_generator.commands.base import check_parameter_in_config_file

__author__ = 'lin'

import click


@cli.command(name='upload-awr',
             help='Upload keyphrases and groups \
             to AWR Cloud using generated keyword file')
@click.argument('gen-kw-file',
                type=click.Path(exists=True), default='keywords.csv')
@click.option('--username', "-u", callback=check_parameter_in_config_file)
@click.option('--password', callback=check_parameter_in_config_file)
@click.option('--project-id', "-p")
@click.pass_context
def upload_awr(ctx, gen_kw_file, username, password, project_id):
    click.echo("running 'assign_groups' command with:")
    click.echo("gen-kw-file = " + gen_kw_file)

    # choose AWR cloud project
    awr_cloud_project = get_awr_cloud_project(password, username, project_id)

    # read generated keyphrases file
    keyphrases, assignations = read_assignations(gen_kw_file)

    # upload keyphrases
    confirm_continue("You are going to add %s keyphrases in AWR Cloud. Are you sure ?" % len(keyphrases))
    awr_cloud_project.add_keywords(keyphrases)
    awr_cloud_project.fetch_keywords()

    # assign groups in AWR cloud
    confirm_continue("You are going to assign %s groups in AWR Cloud. Are you sure ?" % len(assignations))

    assigned_groups = set()
    awr_cloud_project.fetch_groups()
    for group, keyphrases in iter(assignations.items()):
        awr_cloud_project.assign_to_group(keyphrases, group)
        assigned_groups.add(group)

    # delete unused groups
    awr_cloud_project.fetch_groups()
    unused_groups = awr_cloud_project.determine_unused_groups(assigned_groups)

    group_list_display = ",\n".join(
            [
                "- " + group.name for group in unused_groups
            ]
        )

    if (len(unused_groups) != 0):
        confirm_continue("After assignations, the following %s groups remain unused:\n%s\nDo you want to delete them from AWR Cloud ?" % (len(unused_groups), group_list_display))
        awr_cloud_project.delete_groups(unused_groups)

    click.echo("Successfully imported keywords and groups in AWR Cloud")


def confirm_continue(message):
    answer = click.prompt(message + " (y/n)", type=str).lower()

    if answer != 'y':
        click.echo("Quitting")
        exit(0)


"""
    will return
    {group : [keyphrase1, keyphrase2, ...]}
"""


def read_assignations(gen_kw_file):
    assignations = {}
    rows = csv.get_rows(gen_kw_file)
    keyphrases = set()

    def assign(kp, group):
        if group not in assignations:
            assignations[group] = [kp]
        else:
            assignations[group].append(kp)

    for generated_keyphrase in rows:
        kp = generated_keyphrase[0]
        keyphrases.add(kp)
        # assign to lang groups
        langs = generated_keyphrase[1].split("|")
        for lang in langs:
            group_name = "lang_" + lang
            assign(kp, group_name)
        # assign to topics groups
        topics = generated_keyphrase[2].split("|")
        for topic in topics:
            group_name = "topic_" + topic
            assign(kp, group_name)
            for lang in langs:
                assign(kp, group_name + "_" + lang)
        # assign to pattern groups
        group_name = "pattern_" + "-".join(topics)
        assign(kp, group_name)
        for lang in langs:
            assign(kp, group_name + "_" + lang)
        # assign to tag groups
        tags = generated_keyphrase[3].split("|")
        for tag in tags:
            if tag != '':
                group_name = "tag_" + tag.replace(" ", "-")
                assign(kp, group_name)
                for lang in langs:
                    assign(kp, group_name + "_" + lang)
    return (keyphrases, assignations)
