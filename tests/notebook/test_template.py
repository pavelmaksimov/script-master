import pytest
import yaml

from script_master.notebook import Notebook
from script_master.settings import Settings
from script_master.template import render_template, get_variables_map
from tests.factories import NotebookSchemaFactory


@pytest.mark.asyncio
async def test_get_variables_map(variables_json, variables_yaml, variables_text):
    variables_map = await get_variables_map()

    assert variables_map[str(variables_json[0].name)] == variables_json[1]
    assert variables_map[str(variables_yaml[0].name)] == variables_yaml[1]
    assert variables_map[str(variables_text[0].name)] == variables_text[1]


@pytest.mark.asyncio
async def test_render_template(variables_json, variables_yaml):
    key = '{{' + f'variables["{variables_json[0].name}"]["str"]' + '}}'
    val = '{{' + f'variables["{variables_yaml[0].name}"]["list"]' + '}}'
    yaml_text = f"{key}: {val}"
    new_next = await render_template(yaml_text, variables=await get_variables_map())

    assert new_next  == f"{variables_json[1]['str']}: {variables_yaml[1]['list']}"


@pytest.mark.asyncio
async def test_notebook_with_variables_yaml(variables_yaml):
    path = Settings().NOTEBOOK_DIR / "test_notebook.yaml"
    schema = NotebookSchemaFactory().build()
    schema.git.url = '{{' + f'variables["{variables_yaml[0].name}"]["str"]' + '}}'

    with open(path, 'w') as f:
        yaml.dump(schema.dict(), f)

    notebook = await Notebook.from_path(path)
    await notebook.validate()

    assert notebook.schema.git.url == 'name'


@pytest.mark.asyncio
async def test_notebook_with_variables_text(variables_text):
    path = Settings().NOTEBOOK_DIR / "test_notebook.yaml"
    schema = NotebookSchemaFactory().build()
    schema.git.url = '{{' + f'variables["{variables_text[0].name}"]' + '}}'

    with open(path, 'w') as f:
        yaml.dump(schema.dict(), f)

    notebook = await Notebook.from_path(path)
    await notebook.validate()

    assert notebook.schema.git.url == variables_text[1]
