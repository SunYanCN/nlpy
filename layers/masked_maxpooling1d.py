from keras.layers import MaxPooling1D
import keras.backend as K

class MaskedMaxPooling1D(MaxPooling1D):
    """
    Max pooling over sequences that works with masked inputs.
    """
    def __init__(self, **kwargs):
        super(MaskedMaxPooling1D, self).__init__(**kwargs)
        self.supports_masking = True

    def compute_mask(self, inputs, mask=None):
        """Computes an output mask tensor.
        # Arguments
            inputs: Tensor or list of tensors.
            mask: Tensor or list of tensors.
        # Returns
            None or a tensor (or list of tensors,
                one per output tensor of the layer).
        """
        if mask is None:
            return None
        # dimensions of mask should be (batch_size, time_steps)
        assert mask.ndim == 2
        # add a dummy dimension so that the shape is now
        # (batch_size, time_steps, 1)
        mask = K.expand_dims(mask, 2)
        # now add a fake 2nd spatial dimension
        # (batch_size, time_steps, 1, 1)
        mask = K.expand_dims(mask, 3)
        strides = self.strides + (1,)
        pool_size = self.pool_size + (1,)
        mask = K.pool2d(
            mask,
            pool_size=pool_size,
            strides=strides,
            padding=self.padding,
            data_format="channels_last",
            pool_mode='max')
        # get rid of dummy dimensions
        mask = K.squeeze(mask, 3)
        mask = K.squeeze(mask, 2)
        return mask
