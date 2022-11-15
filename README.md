
# DVC: Una herramienta para administrar y versionar experimentos con datos y modelos

Este repositorio demuestra como utilizar DVC para versionar y hacer seguimiento (*tracking*) de archivos binarios, por ejemplo datos y modelos. También veremos como construir pipelines para ejecutar experimentos con un sólo comando. Finalmente veremos como combinar la anterior para realizar y administrar experimentos de ML.

Este repositorio tiene tres tags importantes:

- `blank`: DVC no ha sido configurado
- `dvc-tracked` : DVC configurado para hacer seguimiento de datos 
- `dvc-experiment`: DVC configurado para hacer seguimiento de datos y administrar experimentos

Si desea seguir este tutorial paso a paso sugiero crear una rama (*branch*) desde la etiqueta (*tag*) `blank` con:

    git checkout blank
    git switch -c my-own-dvc-journey

La única referencia para este tutorial es la documentación de DVC: https://dvc.org/. La documentación es excelente, por favor revísenla. 

## Ambiente de desarrollo para DVC

Para hacer este tutorial se necesita un ambiente de Python con DVC y las librerías usuales de *machine learning*. Si no tiene un ambiente de Python, puede prepararlo rápidamente con:

    conda create -n demo python=3.9 pip scikit-learn pandas
    conda activate demo
    pip install -r requirements.txt

Si ya tiene un ambiente y sólo necesita DVC, puede instalarlo con:

    pip install dvc[gdrive]

Por simpleza del tutorial se utilizará *google drive* como servidor de almacenamiento remoto.

**Nota**: Para otras opciones de servidores remotos vea aquí: https://dvc.org/doc/install/linux#install-with-pip, por ejemplo Amazon S3, Microsoft Azure o un equipo personal que se accede por SSH. Si no está seguro sobre cual remoto utilizar puede instalarlos todos con: `pip install dvc[all]`


## Start [tracking data with DVC](https://dvc.org/doc/start/data-management/data-versioning)

**Important:** DVC requires a git tracked folder. 

This repo is already git tracked. If you want to start using DVC on a project that is not tracked you would need to do `git init`

To initialize DVC in a git tracked repo run:

    dvc init
    
This will create a hidden .dvc folder for the DVC configuration file and the `cache` folder in which the different versions of our binaries will live.

To track data we use the [`dvc add`](https://dvc.org/doc/command-reference/add) command. You can either track a single binary or a directory. In the latter case DVC treats the folder as a single data artifact.

Example:

    unzip explorer_ztf_lcs.zip
    dvc add raw_data
    git add .gitignore raw_data.dvc
    git commit -m "raw_data tracked with dvc"
    git push

DVC tracks artifacts by their MD5 hashes which are stored in a `.dvc` file. These files should be git tracked.

## [Trayendo/enviado datos desde/hacia el cache al remoto](https://dvc.org/doc/start/data-management/data-pipelines)

Intente remove un archivo cualquier dentro del directorio `raw_data` y luego ejecute [`dvc pull`](https://dvc.org/doc/command-reference/pull). Los datos que se han perdido se traen (*pull*) desde el *cache*. Si el *cache* no existe, por ejemplo cuando se clona por primera vez el repositorio, entonces `dvc pull` traerá los datos desde el servidor remoto.

**Nota:** Se puede traer los archivos asociados a un artefacto `.dvc` individual con `dvc pull nombre.dvc`. En cambio `dvc pull` a secas traerá todos los artefactos del repositorio.

Github es el servidor remoto para código fuente versionado con `git`. Para respaldar y compartir archivos binarios debemos configurar un servidor remoto para DVC. Los remotos se añaden/configuran/borran con la instrucción [`dvc remote`](https://dvc.org/doc/command-reference/remote#remote)

Para configurar *google drive* como servidor remoto:

    dvc remote add -d mygdrive gdrive://mygdrivefolderID

donde la ID es la secuencia de caracteres que aparece en la URL de la carpeta que queremos utilizar.

Esto crea un remoto por defecto (*default*) en el archivo de configuración `.dvc/config`. Luego, para enviar datos al remoto utilizamos:

    dvc push

La primera vez que ejecutemos este comando en la sesión se abrirá una pestaña en el navegador donde se solicitarán los permisos necesarios para su cuenta de google. 
    
**Nota:** Si tiene problemas con los comandos `push` o `pull` se recomienda agregar el flag `-v` 

**Nota:** Lo anterior es suficiente para uso personal y para una cantidad moderada de archivos. Si se desea usar servicios de Google sin tener que aceptar permisos manualmente se recomienda usar *Google Cloud Project*. Otros servicios en la nube como Azure ponen menos problemas.

## Checking out between "data commits"

Simply change git branches or move to a commit with a different dvc file and checkout with dvc, example:

    git checkout <...>
    dvc checkout

## Making a [data pipeline](https://dvc.org/doc/start/data-management/data-pipelines)

DVC pipelines are `dvc.yaml` files which describe stages that are run sequentially, e.g. data wrangling, feature extraction, model training and metrics computation. Stating this process as a pipeline allows for easier reproducibility and task automation.

You can run the pipeline with the command

    dvc repro

Running this will create a `dvc.lock` file that should be git-tracked, also the results of the pipeline can be dvc-pushed to be shared.

The stages of the pipeline may define dependencies on certain python scripts and data artifacts. DVC detects these changes and execute the needed stages. Stages are defined using the `dvc stage add` command

The commands used to create the stages in this demo were:

    dvc stage add -n parse_raw_data -d src/parse_raw_data.py -d raw_data/ -o data python src/parse_raw_data.py 

    dvc stage add -n compute_features -p features.list -d src/compute_features.py -d data/ -o features/ python src/compute_features.py

    dvc stage add -n train_model -p train.max_depth,train.criterion -d src/train_classifier.py -d features/ -o models/ python src/train_classifier.py

    dvc stage add -n evaluate_model -d src/evaluate_classifier.py -d models/ -d features/ -M metrics.json python src/evaluate_classifier.py


Each flag in `dvc stage add` means:

- `-n` : name of the stage
- `-d` : dependencies of the stage (can be many)
- `-o` : outputs of the stage (can be many and will be dvc-tracked automatically)
- `-p` : parameters for the stage, they should appear in a `params.yaml` file
- `-M` : metrics file (more in this later)

The `params.yaml` might contain model hyperparameters, dataset proportions, random seeds, etc

**Note:** There can be several pipelines in a dvc repo, but only one per folder.

## [Metrics](https://dvc.org/doc/start/data-management/metrics-parameters-plots)

The last stage (evaluate model) set up a git tracked file called `metrics.json` 

In this case `src/evaluate_model.py` computes the f1-score of the trained model and saves this value in that file

We can check the performance of the current evaluation using

    dvc metrics show 

In general we want to iteratively improve our results by tuning and comparing models. We will now see DVC capabilities to track experiments using pipelines and metrics.

**Note:** Metrics can be numerical tables and also plots, see the examples in the dvc documentation

## Experiments 

An ML experiment in DVC is build from pipeline, parameter file and data artifacts. 

The commands for managing experiments start with `dvc exp`

For example:

    `dvc exp show`

Presents a table with the results  commited to `main` andthe current head (`workspace`). The table includes the metrics, parameters and artifact versions.

You can run an experiment with:

    dvc exp run --set-param train.criterion='entropy'

In this case we modified the DT hyperparameter `criterion` at run time. If you do `dvc exp show` again you will say the experiment under `main`

We can set a queue of experiments using the `--queue` flag on `dvc exp run` and then calling

    dvc exp run --run-all --jobs P

where `P` is the amount of parallel tasks

Experiments are not tracked (non-permament). We can update our workspace with a particular experiment using `dvc exp apply` or we can create permament branches for an experiment with `dvc exp branch`. We can clean experiments with `dvc exp gc`. 

**Note:** Experiments can be shared by pushing/pulling them to a remote

