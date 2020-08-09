.PHONY: activate build clean run test
ZIP_FILE=build.zip
CWD=$(shell pwd)

create_env:
	pyenv virtualenv 3.8.3 weight-watchers-env

activate_env:
	pyenv activate weight-watchers-env

install_reqs:
	pip install -r requirements.txt

build:
	cd ~/.pyenv/versions/3.8.3/envs/weight-watchers-env/lib/python3.8/site-packages && \
		zip -r9 ${CWD}/${ZIP_FILE} . && \
		cd ${CWD} && \
		zip -rg ${ZIP_FILE} main.py weight_watchers.py endpoints/

clean:
	rm -rf ./${ZIP_FILE}

run:
	sam local invoke \
		--template template.yaml \
		--event event.json

test:
	pytest tests/

update_lambda:
	aws lambda update-function-code --function-name weight-watchers --zip-file fileb://build.zip
