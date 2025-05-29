from astropy.io import fits

hdr = fits.Header()
hdr['T'] = 170.0
hdr['R0'] = 1.5
hdr['REARTH'] = 6371.0
hdr['AFRHO0'] = 1000.0
hdr['R0'] = 1.0
hdr['K'] = -2.0
hdr['H'] = 10.5
hdr['N'] = 4
hdr['DELTA'] = 1.2
hdr['MK'] = 12.3
hdr['R'] = 1.3
hdr['PV'] = 0.04
hdr['ANGSIZE'] = 2.5
hdr['T'] = 160
hdr['REARTH'] = 6371

hdu = fits.PrimaryHDU(header=hdr)
hdu.writeto('test_data_clean.fits', overwrite=True)
