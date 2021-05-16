

class PipelineContext:
    listening = False
    nodes = []

    @staticmethod
    def register(node):
        PipelineContext.nodes.append(node)
    
    @staticmethod
    def listen():
        PipelineContext.listening = True
        PipelineContext.nodes = []

    @staticmethod
    def close():
        PipelineContext.listening = False
        return PipelineContext.nodes