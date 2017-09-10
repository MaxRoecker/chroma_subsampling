import numpy as np
import cv2
from chroma_subsampling.chroma_subsampling import ChromaSubsampler


def build_ycrcb_test(J, a, b):
    def test(image):
        image_ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
        (y, cr, cb) = (image_ycrcb[:,:,0], image_ycrcb[:,:,1], image_ycrcb[:,:,2])
        sampler = ChromaSubsampler(J=J, a=a, b=b)
        cr_encoded = sampler.encode(cr)
        cb_encoded = sampler.encode(cb)
        encoded_size = y.nbytes + cr_encoded.nbytes + cb_encoded.nbytes
        cr_decoded = sampler.decode(cr_encoded)
        cb_decoded = sampler.decode(cb_encoded)
        decoded_ycrcb = np.dstack((y, cr_decoded, cb_decoded))
        decoded_bgr = cv2.cvtColor(decoded_ycrcb,  cv2.COLOR_YCR_CB2BGR)
        return (decoded_bgr, encoded_size)
    return test


def build_rgb_test(J, a, b):
    def test(image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        (rc, gc, bc) = (image_rgb[:,:,0], image_rgb[:,:,1], image_rgb[:,:,2])
        sampler = ChromaSubsampler(J=J, a=a, b=b)
        r_encoded = sampler.encode(rc)
        g_encoded = sampler.encode(gc)
        b_encoded = sampler.encode(bc)
        encoded_size = r_encoded.nbytes + g_encoded.nbytes + b_encoded.nbytes
        r_decoded = sampler.decode(r_encoded)
        g_decoded = sampler.decode(g_encoded)
        b_decoded = sampler.decode(b_encoded)
        decoded_rgb = np.dstack((r_decoded, g_decoded, b_decoded))
        decoded_bgr = cv2.cvtColor(decoded_rgb,  cv2.COLOR_RGB2BGR)
        return (decoded_bgr, encoded_size)
    return test


if __name__ == '__main__':
    image = cv2.resize(cv2.imread('./rsc/lenna.png'), (256, 256))
    image_size = image.nbytes
    print('Original size (bytes): {}'.format(image_size))

    ratios = [(4, 4, 4), (4, 4, 0), (4, 2, 2), (4, 2, 0), (4, 1, 1), (4, 1, 0)]
    for (J, a, b) in ratios:
        ycrcb_test = build_ycrcb_test(J, a, b)
        rgb_test = build_rgb_test(J, a, b)
        (ycrcb_result, ycrcb_enconded_size) = ycrcb_test(image)
        (rgb_result, rgb_enconded_size) = rgb_test(image)
        ycrcb_enconded_ratio = ycrcb_enconded_size / image_size
        rgb_enconded_ratio = rgb_enconded_size / image_size
        result = np.hstack((image, ycrcb_result, rgb_result))
        test_name = '{}:{}:{}'.format(J, a, b)
        cv2.imshow(test_name, result)
        print('TEST FOR {} -----'.format(test_name))
        print('YCrCb Encoded size (bytes): {} ({}%)'.format(ycrcb_enconded_size, ycrcb_enconded_ratio * 100))
        print('RGB Encoded size (bytes): {} ({}%)'.format(rgb_enconded_size, rgb_enconded_ratio * 100))
        print('')
        char = cv2.waitKey(0)
  
