test:
	pwd
	ls
	export PYTHONPATH=$PYTHONPATH:`pwd`/app
	sh `pwd`/ci/run_tests.sh
#pylint --rcfile=`pwd`/pylint.conf ./app/dao
#pylint --rcfile=`pwd`/pylint.conf ./app/service