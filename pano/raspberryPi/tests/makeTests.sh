export PYTHONPATH=$(pwd)

for x in $(find . -name "*.py")
do
    python3 "$x" -v
done;
