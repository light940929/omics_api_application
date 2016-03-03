##Omics Pipe API Application - A computational API for reproducible next generation sequencing analysis
=============================
[Read more words!](http://aws1niagads.org:8000/about/)

###Usage
####step 1: Make sure you already have set your templates, ingredientgoups info on [/templates api](http://aws1niagads.org:8000/templates)&[/ingredientgroups api](http://aws1niagads.org:8000/ingredientgroups)

####step 2: Build your template on your local path. Please execute  ```buildtemplate.py (-h | --help)``` to know detail options and you will generate your YAML file.

```
   buildtemplate.py get -p <pipelinesid> -i <ingredientgroupsid> -t <templatesid>  -u <username> -e <useremail> > <templatename>.yaml
```

####step 3: Make sure you already have set your modules, pipelinerecipes, userfiles, stepgoups info on [/modules api](http://aws1niagads.org:8000/modules)&[/pipelinerecipes api](http://aws1niagads.org:8000/pipelinerecipes)&[/userfiles api](http://aws1niagads.org:8000/userfiles)&[/stepgroups api](http://aws1niagads.org:8000/stepgroups)

####step 4: Generate your module on your local path. Please execute ```generatemodule.py (-h | --help)``` to know detail options and you will generate your module file. When the file generate your own path, you need to copy this file to the ```~/.local/lib/python2.7/site-packages/omics_pipe/modules/```Advise you to use small letter.

```
    generatemodule.py get -r <pipelinerecipesid> -s <stepsid> -f <userfilesid> -o <resultfilename> > <custom_module_name>.py
```

####step 5: Generate your main file on your local path. Please execute ```linkmodule.py (-h | --help)``` to know detail info. When you get your file, you have to copy this file to the ```~/.local/lib/python2.7/site-packages/omics_pipe/```. Advise you to use capital letter.

```
   linkmodule.py get -r <pipelinerecipesid> -s <stepgroupsid>  > <MAIN_NAME>.py
```

####step 6: Run omics_pipe with a custom pipeline script When you call the omics_pipe function, you will specify the path to your custom script using the command

```
~/.local/bin/omics_pipe custom --custom_script_path ~/omics_sge/omics_pipe/omics_pipe/ --custom_script_name <YOUR_CUSTOM_SCRIPT_NAME> <YAML_FILE_PATH/YAML_FILE_NAME>.yaml
```
