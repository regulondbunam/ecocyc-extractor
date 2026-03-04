# Standard
import pytest
import os

# Mark all tests in this module as integration tests
pytestmark = pytest.mark.integration

# Third-party
# import pythoncyc

# Local

organism: str = "ECOLI"
cyc_host: str = "localhost"
cyc_port: str = "5008"

# Environment variables required by the Pathway Tools connection
os.environ["ORGANISM"] = organism
os.environ["CYC_HOST"] = cyc_host
os.environ["CYC_PORT"] = cyc_port


@pytest.fixture(scope="session")
def pt_connection():
    """
    Create a session-scoped connection to Pathway Tools.

    This fixture attempts to establish a connection to a running
    Pathway Tools server using the environment variables:
    - ORGANISM
    - CYC_HOST
    - CYC_PORT

    If the connection cannot be established, all tests that depend
    on this fixture will be skipped instead of failing.

    Returns
    -------
    Connection
        An active Pathway Tools connection object.
    """

    from ecocyc_extractor.ecocyc.utils.pathway_tools.connection import Connection

    try:
        conn = Connection()
        return conn
    except (ConnectionRefusedError, TimeoutError, OSError) as e:
        pytest.skip(
            f"Pathway Tools is not accessible at {cyc_host}:{cyc_port}. "
            f"Error: {type(e).__name__}: {e}"
        )
    except Exception as e:
        pytest.skip(
            f"Unexpected error while connecting to Pathway Tools: "
            f"{type(e).__name__}: {e}"
        )


def test_connection_is_alive(pt_connection):
    """
    Verify that the Pathway Tools connection fixture was created successfully.

    If this test is executed, it implies that the connection was established
    without errors.
    """
    assert pt_connection is not None


def test_get_frame_object(pt_connection, frame_id: str = "|EG10054|"):
    """
    Retrieve a frame object from Pathway Tools by its frame ID.

    Parameters
    ----------
    frame_id : str
        The Pathway Tools frame identifier to retrieve.

    The test verifies that the returned object is a dictionary,
    which is the expected representation of a frame object.
    Defaults to '|EG10054|' (araC Gene).
    """
    result = pt_connection.get_frame_object(frame_id)
    assert isinstance(result, dict)

def test_get_frame_objects(pt_connection, frame_ids: list = ["|EG10054|", "|EG10054|"]):
    """
    Retrieve a frame object from Pathway Tools by frame IDs list.

    Parameters
    ----------
    frame_ids : list
        The Pathway Tools frame identifiers to retrieve.

    The test verifies that the returned object is a list of dictionaries,
    which is the expected representation of multiple frame objects.
    Defaults to '|EG10054|' (araC Gene).
    """
    result = pt_connection.get_frame_objects(frame_ids)
    assert isinstance(result, list)


def test_fetch_ids_of_all_class_instances(pt_connection, gene_class: str = "|All-Genes|"):
    """
    Retrieve the identifiers of all instances belonging to a given class
    in Pathway Tools.

    This test queries Pathway Tools for all instances of the specified
    class (by default, the special class '|All-Genes|') and verifies that:

    - The returned value is a list
    - The list is not empty
    - Each element in the list is a string representing a frame identifier

    Parameters
    ----------
    pt_connection
        An active Pathway Tools connection fixture.
    gene_class : str, optional
        The Pathway Tools class identifier whose instances will be fetched.
        Defaults to '|All-Genes|'.
    """
    result = pt_connection.get_class_all_instances(gene_class)
    assert isinstance(result, list)
    assert len(result) > 0
    assert isinstance(result[0], str)

