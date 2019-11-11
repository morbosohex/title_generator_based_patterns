 # Title Generator Based Patterns
## Introduction

The title generator provide multiple commands in order to generate and manage a set of titles. this tool has two method to generate titles: firstly,  given a list of *patterns*(designed by user) composed by *keyword_placeholders*,  ones method is  given a list of keywords for each *keyword_placeholder*, the tool generates all titles (= keyword combinations) corresponding to the patterns based on the keywords listed for each *keyword_placeholder*, other is given a list of keywords, these keywords will be classified by many merchandise dictionary, the result after classified by dictionary will composed same as method one.



You can run this command to see the demo of this projects:

```bash
streamlit run https://raw.githubusercontent.com/morbosohex/title_generator_based_patterns/master/TGBP_APP.py
```





Commands:

| Command                                    | Description                                                  |
| ------------------------------------------ | ------------------------------------------------------------ |
| generate --file [keyword_placeholders dir] | Generate titles from an input directory and save it into a file *generated titles file* |
| generate  -k [keyword] -k [keyword]..      | Generate titles from an input keywords and save it into a file *generated titles file* |
| pattern [OPTIONS]                          | Generate patterns from given certain hyperparameter          |

## Command synthax
To get general help on the title generator:
```shell
title
```

To know options for each commands:
```shell
title [COMMAND] --help
```

## Installation

Download or clone the repository from github.

Then:

```
cd <Package ROOT_DIR>
```

Then:

```shell
sudo pip install --editable .
```



## Quick Start

#### Generate Patterns

- Firstly, run `title pattern`will generate a set of patterns based given certain dictionaries, user can add dictionary file to folder `<Package Root_DIR>/title_generator/kw_generator/dic/`

- After add some dictionary files, run below commands to generate patterns based type of dictionary

  ```bash
  title pattern [option]
  ```

  `title pattern`have some options to control the generation of patterns, just like hyper parameter of machine learning, you can tune those parameters to generate different kind of patterns, details in below:

  ```bash
  Usage: title pattern [OPTIONS]
  
    Generate patterns from given certain hyperparameter
  
  Options:
    -i, --init-label-num INTEGER RANGE number of labels in each pattern of noduplicated label
                                    
    -m, --must_include_label TEXT   label must contained in each unique pattern
    
    -l, --min_words_num INTEGER RANGE expand pattern setup, minimum words in each pattern
                                    
    -h, --max_words_num INTEGER RANGE expand pattern setup, maximum words in each pattern
                                    
    -u, --max_num_unique_label INTEGER RANGE maximum unique labels in each pattern
                                    
    -p, --priority_limit INTEGER RANGE lowest priority of each pattern, `1` means highest
                                    
    -o, --output TEXT patterns file to output (default ='./patterns.csv')
    --help  Show this message and exit.
  ```
  
  
  
- If you don't want tune these parameters by yourself, you can just run `title pattern` to quicklook how it goes

- After you run `title pattern`, you will get a folder `patterns` in `<root package dir>`which is a backup folder for patterns you generated, meanwhile you will get a csv file `patterns.csv` in `<root package dir> `, this csv file will be used to generate title later.

#### Generate Titles

- Run title generator as `file` mode, you need to put keywords after classified into each csv file in `keyword_placeholders`folder, after you done that, run commands below you will see the result in `file`mode , also you can add `--verbose=True`to print some info

  ```bash
  title generate --file
  ```

- Run title generator as `text`mode, and `text` mode is default mode, this time you need to input keywords argument by hand, such as below:

  - run text mode by **default value**, also you can add `--verbose=True`to print some info

  ```bash
  title generate 
  ```

  - run text mode by **given a set of keyword**, , also you can add `--verbose=True`to print some info

  ```bash
  title generate -k 'iphone xr' -k 'apple' -k '128GB' -k '32GB' -k 'Mobile' -k 'Smartphone'
  ```

  

## More information about the *generate* command

A short example.

**Given ...**

A project directory with the following structure:

```
ROOT_DIR
|
+-- patterns.csv
+-- keyword_placeholders
    +-- [placeholder_1].csv
    +-- ...
```

`patterns.csv` file which lists keyphrases *patterns*, which are composed by *keyword_placeholders* separated by spaces (or plus sign for compound words). Note how patterns are attributed to one or many language (the same will go for placeholder files):

Note: below patterns just example, if you want to test you can run `title pattern`to generate you own patterns.

```
pattern,languages,tag,example keyphrase
brand category,en,priority-1|words-2,''
color category,en,priority-1|words-2,'green lamp'
color style,en,priority-1|words-2,''
style category,en,priority-1|words-2,''
brand color size other,en,priority-1|words-4,''
brand color other,en,priority-1|words-3,''
brand color style,en,priority-1|words-3,''
brand style category,en,priority-1|words-3,''
color style brand category,en,priority-3|words-4,''

```

A `/keyword_placeholders/` folder of `[PLACEHOLDER].csv` files detailing the real keywords behind each placeholder (in the above defined patterns, there are three placeholders: `brand`, `category`, `color`,`group`,and `style`):

`/keyword_placeholders/brand.csv`:

```
keyword,language
apple,en
```

`/keyword_placeholders/category.csv`:

```
keyword,languages
laptop,en
computer,en
```

`/keyword_placeholders/color.csv`:

```
keyword,languages
gray,en
silver,en
```

`/keyword_placeholders/group.csv`:

```
keyword,languages

```

`/keyword_placeholders/color.csv`:

```
keyword,language
Macbook Air,en
Macbook Pro,en
```

`/keyword_placeholders/other.csv`:

```
keyword,language
15 inch,en
13 inch,en
```



... the script will output all possible keyword combinations in the following `titles.csv` file:**


```
keyphrase,lang,topics,tags
Macbook Air computer,en,category|style,priority-1|words-2
Macbook Air laptop,en,category|style,priority-1|words-2
Macbook Pro computer,en,category|style,priority-1|words-2
Macbook Pro laptop,en,category|style,priority-1|words-2
apple Macbook Air computer,en,brand|category|style,priority-1|words-3
apple Macbook Air laptop,en,brand|category|style,priority-1|words-3
apple Macbook Pro computer,en,brand|category|style,priority-1|words-3
apple Macbook Pro laptop,en,brand|category|style,priority-1|words-3
apple computer,en,brand|category,priority-1|words-2
apple gray 13 inch,en,brand|color|other,priority-1|words-3
apple gray 15 inch,en,brand|color|other,priority-1|words-3
apple gray Macbook Air,en,brand|color|style,priority-1|words-3
apple gray Macbook Pro,en,brand|color|style,priority-1|words-3
apple laptop,en,brand|category,priority-1|words-2
apple silver 13 inch,en,brand|color|other,priority-1|words-3
apple silver 15 inch,en,brand|color|other,priority-1|words-3
apple silver Macbook Air,en,brand|color|style,priority-1|words-3
apple silver Macbook Pro,en,brand|color|style,priority-1|words-3
gray Macbook Air,en,color|style,priority-1|words-2
gray Macbook Air apple computer,en,brand|category|color|style,priority-3|words-4
gray Macbook Air apple laptop,en,brand|category|color|style,priority-3|words-4
gray Macbook Pro,en,color|style,priority-1|words-2
gray Macbook Pro apple computer,en,brand|category|color|style,priority-3|words-4
gray Macbook Pro apple laptop,en,brand|category|color|style,priority-3|words-4
gray computer,en,category|color,priority-1|words-2
gray laptop,en,category|color,priority-1|words-2
silver Macbook Air,en,color|style,priority-1|words-2
```

## Group management

### pattern groups


It is possible to attribute groups to patterns – in our above example, we assign the 'prio-1' and 'prio-2' groups to the patterns. Multiple groups can be associated to a pattern by separating them with "|".


