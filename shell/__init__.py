from dataclasses import dataclass, field


@dataclass
class ShellResult:
    success: bool = field(default_factory=lambda : False)
    stdout: str = field(default_factory=lambda : None)
    stderr: str = field(default_factory=lambda : None)
    msg: str = field(default_factory=lambda : None)
