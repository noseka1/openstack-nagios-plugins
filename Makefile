
all:
	python setup.py build

install:
	python setup.py install

clean:
	python setup.py clean
	rm -rf build
	rm -rf develop
	rm -rf dist
	rm -rf openstacknagios.egg-info

test:
	python setup.py test

develop:
	python -m virtualenv develop
	develop/bin/python setup.py develop

run_help:
	check_nova-hypervisors --help
	check_nova-services --help
	check_neutron-agents --help
	check_neutron-floatingips --help
	check_cinder-services --help

