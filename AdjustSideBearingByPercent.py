#MenuTitle: Change Side Bearing by Percentage
# -*- coding: utf-8 -*-
__doc__="""
Adjust sidebearing by percentage
"""
import vanilla
import GlyphsApp

def changeSB(sideBaring, percentage):
	factor = float(percentage)/100
	if sideBaring < 0:
		if factor > 1 < 1.5:
			factorForNegatives = (1-factor)+1
			#print "(+)factor =", factor
			#print "(-)factor (f1~1.5) =", factorForNegatives
			factor = factorForNegatives
		elif factor > 1.5:
			factorForNegatives = -(-factor+2)
			#print "(+)factor =", factor
			#print "(-)factor (f>1.5) =", factorForNegatives
			factor = factorForNegatives
		else:
			factorForNegatives = (-factor+2)
			#print "(+)factor =", factor
			#print "(-)factor (else) =", factorForNegatives
			factor = factorForNegatives
	newSideBaring = sideBaring * factor
	return newSideBaring	

class ChangeSideBearingByPercentage( object ):
	def __init__( self ):
		# Window 'self.w':
		windowWidth  = 260
		windowHeight = 180
		windowWidthResize  = 0 # user can resize width by this value
		windowHeightResize = 0   # user can resize height by this value
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Change Side Bearings by percentage", # window title
			minSize = ( windowWidth, windowHeight ), # minimum size (for resizing)
			maxSize = ( windowWidth + windowWidthResize, windowHeight + windowHeightResize ), # maximum size (for resizing)
			autosaveName = "com.nsilva.ChangeSideBearingByPercentage.mainwindow" # stores last window position and size
		)
		# UI elements:         		  margings: left       top   width  height
		self.w.percentage    = vanilla.EditText((10+25,    10+5,    40, 25), "100",                   sizeStyle='regular')
		self.w.Instructions  = vanilla.TextBox( (10+60+16, 10+7,   150, 18), "% of the current space",sizeStyle='regular')
		self.w.Description   = vanilla.TextBox( (10+60+15, 10+27,  170, 14), "100% is the current distance",  sizeStyle='small')
		self.w.LSB           = vanilla.CheckBox((10+25,    10+85,  -10, 20), "LSB",   value=True,     sizeStyle='small')
		self.w.RSB           = vanilla.CheckBox((10+135,   10+85,  -10, 20), "RSB",   value=True,     sizeStyle='small')
		self.w.TSB           = vanilla.CheckBox((10+60+17, 10+65,  -10, 20), "TSB",   value=False,    sizeStyle='small')
		self.w.BSB           = vanilla.CheckBox((10+60+17, 10+105, -10, 20), "BSB",   value=False,    sizeStyle='small')
		self.w.replaceButton = vanilla.Button(  (-115,       -32,  -15, 17), "Change",                sizeStyle='small', \
					callback=self.ChangeSideBearingByPercentageMain)
		self.w.setDefaultButton( self.w.replaceButton )
				
		# Load Settings:
		if not self.LoadPreferences():
			print "Note: 'Adjust sidebearing by percentage' could not load preferences. Will resort to defaults"
		
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()

	def SavePreferences( self, sender ):
		try:
			Glyphs.defaults["com.nsilva.ChangeSideBearingByPercentage.percentage"] = self.w.percentage.get()
			Glyphs.defaults["com.nsilva.ChangeSideBearingByPercentage.LSB"]        = self.w.LSB.get()
			Glyphs.defaults["com.nsilva.ChangeSideBearingByPercentage.RSB"]        = self.w.RSB.get()
			Glyphs.defaults["com.nsilva.ChangeSideBearingByPercentage.TSB"]        = self.w.TSB.get()
			Glyphs.defaults["com.nsilva.ChangeSideBearingByPercentage.BSB"]        = self.w.BSB.get()
		except:
			return False

	def LoadPreferences( self ):
		try:
			self.w.percentage.set( Glyphs.defaults["com.nsilva.ChangeSideBearingByPercentage.percentage"] )
			self.w.LSB.set(        Glyphs.defaults["com.nsilva.ChangeSideBearingByPercentage.LSB"] )
			self.w.RSB.set(        Glyphs.defaults["com.nsilva.ChangeSideBearingByPercentage.RSB"] )
			self.w.TSB.set(        Glyphs.defaults["com.nsilva.ChangeSideBearingByPercentage.TSB"] )
			self.w.BSB.set(        Glyphs.defaults["com.nsilva.ChangeSideBearingByPercentage.BSB"] )
		except:
			return False	
		#return True
	
	def ChangeSideBearingByPercentageMain( self, sender ):
		try:
			percentage = float(self.w.percentage.get()) # percentage value
			ActiveLSB  = self.w.LSB.get()
			ActiveRSB  = self.w.RSB.get()
			ActiveTSB  = self.w.TSB.get()
			ActiveBSB  = self.w.BSB.get()

			for layer in font.selectedLayers:
				if all(bound != 0 for bound in [layer.bounds.size.width, layer.bounds.size.height]):
					if any(Actived == True for Actived in [ActiveLSB, ActiveRSB, ActiveTSB, ActiveBSB]):
						layer.parent.beginUndo()
						print "\n"+layer.parent.name+":"
						if ActiveLSB:
							LSB = layer.LSB
							newLSB = changeSB(LSB, percentage)
							layer.LSB = newLSB
							print "LSB: %s => %s" % (LSB, newLSB)
						if ActiveRSB:
							RSB = layer.RSB
							newRSB = changeSB(RSB, percentage)
							layer.RSB = newRSB
							print "RSB: %s => %s" % (RSB, newRSB)
						if ActiveTSB:
							TSB = layer.TSB
							newTSB = changeSB(TSB, percentage)
							layer.TSB = newRSB
							print "TSB: %s => %s" % (TSB, newRSB)
						if ActiveBSB:
							BSB = layer.BSB
							newBSB = changeSB(BSB, percentage)
							layer.BSB = newRSB
							print "BSB: %s => %s" % (BSB, newRSB)
						layer.parent.endUndo()
					if all(Actived == False for Actived in [ActiveLSB, ActiveRSB, ActiveTSB, ActiveBSB]):
						print "You have not choosen sidebarings to modify"	
				else:
					print layer.parent.name, "\b:\nIt is a space character"

			#if not self.SavePreferences( self ):
			#	print "Note: 'Change Side Bearing by Percentage' could not write preferences."
			
			self.w.close() # delete if you want window to stay open
		except Exception, e:
			# brings macro window to front and reports error:
			Glyphs.showMacroWindow()
			print "Change Side Bearing by Percentage Error: %s" % e


# brings macro window to front and clears its log:
Glyphs.clearLog()
Glyphs.showMacroWindow()
ChangeSideBearingByPercentage()
