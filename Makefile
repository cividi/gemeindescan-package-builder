.PHONY: snapshots

all: snapshots/${PROJECT}

init:
	mkdir ${PROJECT} && mkdir ${PROJECT}/data && mkdir ${PROJECT}/snapshots
	cp sample-project/sample-project.yml ${PROJECT}/${PROJECT}.yml

snapshots/%:
	python3 package-builder.py -p $*