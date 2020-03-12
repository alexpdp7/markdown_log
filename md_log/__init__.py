import panflute as pf


def bp():
    import sys

    sys.stdin = open("/dev/tty")
    import pdb

    pdb.set_trace()


def prepare(doc):
    pass


def action(elem, doc):
    pass


def finalize(doc):
    pass


def main(doc=None, input_stream=None, output_stream=None):
    return pf.run_filter(
        action,
        prepare=prepare,
        finalize=finalize,
        doc=doc,
        input_stream=input_stream,
        output_stream=output_stream,
    )


if __name__ == "__main__":
    main()
