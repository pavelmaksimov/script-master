from pydantic_factories import ModelFactory

from script_master.notebook import NotebookSchema


class ScheduleSchemaFactory(ModelFactory):
    __model__ = NotebookSchema.WorkSchema.ScheduleSchema

    start_time = None
    timezone = None
    fill_missing = False


class WorkSchemaFactory(ModelFactory):
    __model__ = NotebookSchema.WorkSchema

    schedule = ScheduleSchemaFactory


class PythonScriptSchemaFactory(ModelFactory):
    __model__ = NotebookSchema.ScriptSchemas.PythonScriptSchema

    python_options = []
    python_file = "main.py"
    arguments = []
    options = {}
    env = {}
    cwd = None


class NotebookSchemaFactory(ModelFactory):
    __model__ = NotebookSchema

    work = WorkSchemaFactory
    script = PythonScriptSchemaFactory
