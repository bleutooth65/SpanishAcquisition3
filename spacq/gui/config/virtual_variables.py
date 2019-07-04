import wx

# TODO: replace 6 with some variable
"""
An interface for defining virtual swept variables and writing to
real resources.
"""
class MultipleVariableConfigPanel(wx.Panel):
	def __init__(self, parent, *args, **kwargs):
		wx.Panel.__init__(self, parent, *args, **kwargs)

		# Panel
		multiple_static_box = wx.StaticBox(self, label= 'Virtual Variable Setup')
		# sizer_box = wx.StaticBoxSizer(multiple_static_box, wx.VERTICAL)

		panel_box = wx.StaticBoxSizer(multiple_static_box,wx.VERTICAL)
		# sizer_box.Add(panel_box)
		# self.current_count = 4

		count_setup = wx.BoxSizer(wx.HORIZONTAL)
		panel_box.Add(count_setup, flag=wx.ALL, border=5)
		# TODO: determine max count
		label = wx.StaticText(self, label='Number of Virtual Variables')
		self.var_count = wx.SpinCtrl(self, min=1, initial=2, max=6)
		button = wx.Button(self, label='Update')
		self.Bind(wx.EVT_BUTTON, self.OnUpdate, button)

		count_setup.Add(label,flag=wx.ALL, border=5)
		count_setup.Add(self.var_count, flag=wx.ALL, border=5)
		count_setup.Add(button, flag=wx.ALL, border=5)

		value_setup = wx.BoxSizer(wx.HORIZONTAL)
		panel_box.Add(value_setup, flag=wx.ALL, border=5)

		label_setup = wx.BoxSizer(wx.VERTICAL)
		value_setup.Add(label_setup, flag=wx.EXPAND|wx.ALL, border=5)
		label_setup.Add(wx.StaticText(self, label='Name'),
				flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, border=5)
		label_setup.Add(wx.StaticText(self, label='Initial:'),
				flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, border=5)
		label_setup.Add(wx.StaticText(self, label='Final:'),
				flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, border=5)
		label_setup.Add(wx.StaticText(self, label='Steps:'),
				flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, border=5)
		label_setup.Add(wx.StaticText(self, label='Order:'),
				flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, border=5)

		# for i in range(0,self.variable_count.GetValue()):
		self.name_value = [None]*6
		self.start_value = [None]*6
		self.end_value = [None]*6
		self.step_value = [None]*6
		self.order_value = [None]*6

		for i in range(0,6):
			mini_setup = wx.BoxSizer(wx.VERTICAL)
			self.name_value[i] = wx.TextCtrl(self, value="VirtVar{0}".format(i))
			mini_setup.Add(self.name_value[i], flag=wx.EXPAND|wx.ALL, border=5)
			self.start_value[i] = wx.TextCtrl(self, value="1")
			mini_setup.Add(self.start_value[i], flag=wx.EXPAND|wx.ALL, border=5)
			self.end_value[i] = wx.TextCtrl(self, value="2")
			mini_setup.Add(self.end_value[i], flag=wx.EXPAND|wx.ALL, border=5)
			self.step_value[i] = wx.SpinCtrl(self, min=1, initial=3, max=1e9)
			mini_setup.Add(self.step_value[i], flag=wx.EXPAND|wx.ALL, border=5)
			self.order_value[i] = wx.SpinCtrl(self, min=1, initial=1, max=1e9)
			mini_setup.Add(self.order_value[i], flag=wx.EXPAND|wx.ALL, border=5)

			value_setup.Add(mini_setup, flag=wx.EXPAND|wx.ALL, border=5)

		self.SetSizerAndFit(panel_box)

	def OnUpdate(self, evt=None):
		EnableCount = self.var_count.Value
		for i in range(0,EnableCount):
			self.name_value[i].Show()
			self.start_value[i].Show()
			self.end_value[i].Show()
			self.step_value[i].Show()
			self.order_value[i].Show()
		for i in range(EnableCount,6):
			self.name_value[i].Hide()
			self.start_value[i].Hide()
			self.end_value[i].Hide()
			self.step_value[i].Hide()
			self.order_value[i].Hide()

	def GetValue(self):
		try:
			starts = [float(x.Value) for x in self.start_value]
		except ValueError:
			raise ValueError('Invalid initial value.')
		try:
			ends = [float(x.Value) for x in self.end_value]
		except ValueError:
			raise ValueError('Invalid initial value.')

		names = [x.Value for x in self.name_value]
		steps = [x.Value for x in self.step_value]
		orders = [x.Value for x in self.order_value]

		return names, starts, ends, steps, orders

class DependentVariableConfigPanel(wx.Panel):
	def __init__(self, parent, *args, **kwargs):
		wx.Panel.__init__(self, parent, *args, **kwargs)

		static_box = wx.StaticBox(self, label='Dependent Variable Setup')
		static_panel_box = wx.StaticBoxSizer(static_box, wx.VERTICAL)

		count_setup = wx.BoxSizer(wx.HORIZONTAL)
		static_panel_box.Add(count_setup, flag=wx.ALL, border=5)
		# TODO: determine max count
		label = wx.StaticText(self, label='Number of Virtual Variables')
		self.dependent_count = wx.SpinCtrl(self, min=1, initial=2, max=6)
		button = wx.Button(self, label='Update')
		self.Bind(wx.EVT_BUTTON, self.OnUpdate, button)

		count_setup.Add(label, flag=wx.ALL, border = 5)
		count_setup.Add(self.dependent_count, flag=wx.ALL, border = 5)
		count_setup.Add(button, flag=wx.ALL, border = 5)


		panel_box = wx.FlexGridSizer(3,2)

		self.name_value = [None]*6
		self.expression_value = [None]*6
		self.equal_bar = [None]*6
		self.enable = [True]*6

		for i in range(0,6):
			unit_box = wx.BoxSizer(wx.HORIZONTAL)
			self.name_value[i] = wx.TextCtrl(self, value="RealVar{0}".format(i))
			unit_box.Add(self.name_value[i], flag=wx.EXPAND|wx.ALL, border=5)
			self.equal_bar[i] = wx.StaticText(self, label=' = ')
			unit_box.Add(self.equal_bar[i], flag=wx.ALL)
			self.expression_value[i] = wx.TextCtrl(self)
			unit_box.Add(self.expression_value[i], flag=wx.EXPAND|wx.ALL, border=5)

			panel_box.Add(unit_box, flag=wx.EXPAND|wx.ALL, border=5)

		static_panel_box.Add(panel_box, flag=wx.EXPAND|wx.ALL, border=5)
		self.SetSizerAndFit(static_panel_box)

	def OnUpdate(self, evt=None):
		EnableCount = self.dependent_count.Value
		for i in range(0,EnableCount):
			self.name_value[i].Show()
			self.expression_value[i].Show()
			self.equal_bar[i].Show()
			self.enable[i] = True

		for i in range(EnableCount,6):
			self.name_value[i].Hide()
			self.expression_value[i].Hide()
			self.equal_bar[i].Hide()
			self.enable[i] = False

	def GetValue(self):
		names = [x.Value for x in self.name_value]
		expressions = [x.Value for x in self.expression_value]

		return names, expressions
