# pyvipe

* [INTRODUCTION](#introduction)
* [INSTALLATION](#installation)
    * [PIP](#pip)
    * [MANUAL_INSTALLATION](#manual-installation)
* [USAGE](#usage)
* [ENVIRONMENT_VARIABLES](#environment-variables)
* [FAQ](#faq)
* [CHANGELOG](#changelog)
* [CONTRIBUTION](#contribution)

## INTRODUCTION

**pyvipe** is a Python port of [vipe](http://joeyh.name/code/moreutils/).
**pyvipe**'s command is `vipe`

This project is a by-product of [trrc](https://github.com/Constantin1489/trrc) feature development.

## INSTALLATION

### pip

`pip install pyvipe`

### Manual Installation

`pip install .`

## USAGE

```
command1 | vipe | command2
```

Use `--suffix` to apply file syntax highlighting.

### pyvipe special options

If you edit such a CRLF PIPE but want vipe to print it as a universial newline, then use `--universal-newline`. This option is for a Windows generated text file.

## Environment Variables

**pyvipe** chooses the editor to use with the environment variable `$VISUAL`. If it is unset, it uses `$EDITOR`. If both are unset, it uses  `/usr/bin/editor` if it exists. If none of those work, it defaults to vi.

## FAQ

### Editor exited nonzero, aborting.

In general, editor can exit with nonzero when you execute some command for various purposes. e.g preventing git rebase.
But if you didn't execute the command but the editor exited with nonzero, it may be because
of wrong user configuration for the editor.

For vi, you can debug it with `EDITOR='vi -u NONE vipe'`

## Changelog

| Version | Note                     | 
|:--------|:-------------------------|
| HEAD    | add universal-newline option. support editor variable with option. | 
| 0.1.3    | fix shell completion. | 
| 0.1.2    | add suffix option. fix error. | 
| 0.1.1   | init                     | 

## CONTRIBUTION

If it doesn't work as original [vipe](http://joeyh.name/code/moreutils/), then it's a bug.

## Thanks to

[Nick ODell](https://stackoverflow.com/a/76527291/20307768)
