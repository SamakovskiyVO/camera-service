from zcm_types import frame_quality as fq

def test_default():
    msg = fq.ZcmFrameQuality()
    msg.timestamp = 123
    msg.frame_id  = 1
    msg.quality_probs = [0.]*7
    msg.alert_flag = False
    msg.dominant_defect = "good"
    assert msg.frame_id == 1
