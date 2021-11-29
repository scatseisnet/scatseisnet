# import scatseisnet as ssn
import pytest
import subprocess

def test_dataset():

    p = subprocess.Popen("scatnet inventory --datapath ./data/YH.DC06..BH{channel}_{tag}.sac", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    print(output)
    
    p = subprocess.Popen("scatnet transform", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    print(output)
    
    p = subprocess.Popen("scatnet features", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    print(output)
    
    p = subprocess.Popen("scatnet linkage", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    print(output)

# def test_covariance():

    ##read ObsPy's example stream
    # stream = obspy.read()
    # window_duration_sec = 1.0
    # average = 5
    # times, frequencies, covariances = csn.covariancematrix.calculate(
        # stream, window_duration_sec, average
    # )

    # assert covariances.all() != None

    ##test spectral width
    # spectral_width = covariances.coherence(kind="spectral_width")
    # assert spectral_width.all() != None

    ##test coherence
    # coherence = covariances.coherence(kind="coherence")
    # assert coherence.all() != None

    # with pytest.raises(ValueError):
        # covariances.coherence(kind="none")

    ##test eigenvectors
    # eigenvectors = covariances.eigenvectors()
    # assert eigenvectors.all() != None

    ##test upper triangular
    # triu = covariances.triu()
    # assert triu.all() != None


# def test_arraystream():

    # stream = csn.arraystream.read()

    ##test cut
    # stream.cut(
        # starttime=stream[0].stats.starttime + 1, endtime=stream[0].stats.endtime - 1
    # )

    ##test synchronize
    # stream.synchronize()

    ##test all preprocessing methods
    # stream.preprocess()  # default preprocessing
    # stream.preprocess(domain="spectral")  # default method for spectral whitening
    # stream.preprocess(domain="spectral", method="onebit")
    # stream.preprocess(domain="spectral", method="smooth")
    # stream.preprocess(
        # domain="spectral", method="smooth", smooth_length=33, smooth_order=2
    # )
    # stream.preprocess(domain="temporal")  # default method for temporal normalization
    # stream.preprocess(domain="temporal", method="onebit")
    # stream.preprocess(domain="temporal", method="smooth")
    # stream.preprocess(domain="temporal", method="mad")

    ##test times
    # stream.times()
