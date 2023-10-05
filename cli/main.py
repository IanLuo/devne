import typer

def main(action: str):
    '''
  1. dashboard
  2. configure
  3. clock
    '''
    print(f"{action}")

if __name__ == "__main__":
    typer.run(main)
