import argparse

parser = argparse.ArgumentParser()
parser.add_argument("groundtruth")
parser.add_argument("result")
args = parser.parse_args()

print(args.groundtruth)
print(args.result)
