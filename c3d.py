import c3d

reader = c3d.Reader(open('062_00048_Accelerated walking_Gauche001', 'rb'))
for i, points, analog in reader.read_frames():
    print('frame {}: point {}, analog {}'.format(
        i, points.shape, analog.shape))