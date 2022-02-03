import tkinter as tk
from tkinter import ttk
from decimal import Decimal
from pathlib import Path
import re

class Onlydigits(ttk.Entry):
    def __init__(self, parent, *args, **kwargs):
      super().__init__(parent, *args, **kwargs)
      self.configure(
        validate='all',
        validatecommand=(self.register(self.validate_digit), '%P'),
        )
    def validate_digit(self, input):
      if input.isdigit():
        return True 
      elif input is "":
        return True
      else:
        return False

class Onechar(ttk.Entry):
    def __init__(self, parent, *args, **kwargs):
      super().__init__(parent, *args, **kwargs)
      self.configure(
        validate='all',
        validatecommand=(self.register(self.validate_len), '%P'),
        )
    def validate_len(self, input):
      return len(input) <= 1

class Validatedconv(ttk.Entry):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.configure(
        validate='all',
        validatecommand=(self.register(self.validate), '%P'),
        )
  def validate(input_number, **kwargs):
      return bool(re.match(r"\d+.\d+e[-+]\d+", input_number))

      input_number = "5.0e-8"
      valid = is_valid(input_number)
      return True
      input_number = "5.0ae-8"
      valid = is_valid(input_number)
      return False
 
class Decimalentry(ttk.Entry):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.configure(
        validate='all',
        validatecommand=(self.register(self.validate), '%P'),
        )
  def validate(self, inp):
    try:
        return True if inp == '' else float(inp) <= 100 
    except:
        return False

class Fourchar(ttk.Entry):
    def __init__(self, parent, *args, **kwargs):
      super().__init__(parent, *args, **kwargs)
      self.configure(
        validate='all',
        validatecommand=(self.register(self._validate), '%P'),
        )
    def _validate(self, proposed):
      return len(proposed) <= 4


