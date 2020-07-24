import torch
from torch import nn


class ValueHeads(nn.Module):
    def __init__(self, stream_names, input_size, output_size=1):
        super().__init__()
        self.stream_names = stream_names
        _value_heads = {}

        for name in stream_names:
            value = nn.Linear(input_size, output_size)
            _value_heads[name] = value
        self.value_heads = nn.ModuleDict(_value_heads)

    def forward(self, hidden):
        value_outputs = {}
        for stream_name, head in self.value_heads.items():
            value_outputs[stream_name] = head(hidden).squeeze(-1)
        return (
            value_outputs,
            torch.mean(torch.stack(list(value_outputs.values())), dim=0),
        )
