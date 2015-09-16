export PYTHONPATH=$(pwd)

for x in $(find . -name "*.py")
do
    python "$x" -v
done;
