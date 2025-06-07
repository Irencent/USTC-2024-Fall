import numpy as np
import matplotlib.pyplot as plt

# First, we implement the DCT and IDCT
class DCTTransform:
    def __init__(self):
        # Initialize 2D cosine lookup tables
        self.cos_table = np.zeros((8, 8))
        for i in range(8):
            for j in range(8):
                self.cos_table[i, j] = np.cos((2*j + 1) * i * np.pi / 16)

    def get_scale_factor(self, u, v):
        """Get scaling factor C(u)C(v)/4"""
        cu = 1/np.sqrt(2) if u == 0 else 1
        cv = 1/np.sqrt(2) if v == 0 else 1
        return (cu * cv) / 4

    def forward_dct_2d(self, block):
        """Implement 2D DCT"""
        result = np.zeros((8, 8))
        
        for u in range(8):
            for v in range(8):
                sum_val = 0
                for x in range(8):
                    for y in range(8):
                        sum_val += block[x, y] * \
                                 self.cos_table[u, x] * \
                                 self.cos_table[v, y]
                
                result[u, v] = self.get_scale_factor(u, v) * sum_val
        
        return result

    def inverse_dct_2d(self, dct_block):
        """Implement 2D IDCT"""
        result = np.zeros((8, 8))
        
        for x in range(8):
            for y in range(8):
                sum_val = 0
                for u in range(8):
                    for v in range(8):
                        sum_val += self.get_scale_factor(u, v) * \
                                 dct_block[u, v] * \
                                 self.cos_table[u, x] * \
                                 self.cos_table[v, y]
                
                result[x, y] = sum_val
        
        return result
    
class HuffmanCoding:
    def __init__(self):
        # Initialize DC and AC Huffman tables from the provided reference
        self.dc_table = {
            0: '00',
            1: '010', 
            2: '011', 
            3: '100', 
            4: '101', 
            5: '110',
            6: '1110', 
            7: '11110', 
            8: '111110', 
            9: '1111110',
            10: '11111110', 
            11: '111111110'
        }
        
        # Initialize AC table 
        self.ac_table = {
            (0, 0): '1010',      # EOB
            (0, 1): '00',
            (0, 2): '01', 
            (0, 3): '100',
            (0, 4): '1011',
            (0, 5): '11010',
            (0, 6): '1111000',
            (0, 7): '11111000',
            (0, 8): '1111110110',
            (0, 9): '1111111110000010',
            (0, 10): '1111111110000011',
            (1, 1): '1100',
            (1, 2): '11011',
            (1, 3): '1111001',
            (1, 4): '111110110',
            (1, 5): '11111110110',
            (1, 6): '1111111110000100',
            (1, 7): '1111111110000101',
            (1, 8): '1111111110000110',
            (1, 9): '1111111110000111',
            (1, 10): '1111111110001000',
            (2, 1): '11100',
            (2, 2): '11111001',
            (2, 3): '1111110111',
            (2, 4): '111111110100',
            (2, 5): '111111111001001',
            (2, 6): '111111111001010',
            (2, 7): '1111111110001011',
            (2, 8): '111111111001100',
            (2, 9): '111111111001101',
            (2, 10): '111111111001110',
            (3, 1): '111010',
            (3, 2): '111110111',
            (3, 3): '111111110101',
            (3, 4): '1111111110001111',
            (3, 5): '1111111110010000',
            (3, 6): '1111111110010001',
            (3, 7): '1111111110010010',
            (3, 8): '1111111110010011',
            (3, 9): '1111111110010100',
            (3, 10): '1111111110010101',
            (4, 1): '111011',
            (4, 2): '1111111000',
            (4, 3): '1111111110010110',
            (4, 4): '1111111110010111',
            (4, 5): '1111111110011000',
            (4, 6): '1111111110011001',
            (4, 7): '1111111110011010',
            (4, 8): '1111111110011011',
            (4, 9): '1111111110011100',
            (4, 10): '1111111110011101',
            (5, 1): '1111010',
            (5, 2): '11111110111',
            (5, 3): '1111111110011110',
            (5, 4): '1111111110011111',
            (5, 5): '1111111110100000',
            (5, 6): '1111111110100001',
            (5, 7): '1111111110100010',
            (5, 8): '1111111110100011',
            (5, 9): '1111111110100100',
            (5, 10): '1111111110100101',
            (6, 1): '1111011',
            (6, 2): '111111110110',
            (6, 3): '1111111110100110',
            (6, 4): '1111111110100111',
            (6, 5): '1111111110101000',
            (6, 6): '1111111110101001',
            (6, 7): '1111111110101010',
            (6, 8): '1111111110101011',
            (6, 9): '1111111110100100',
            (6, 10): '1111111110100101',
            (7, 1): '11111010',
            (7, 2): '111111110111',
            (7, 3): '1111111110101110',
            (7, 4): '1111111110101111',
            (7, 5): '1111111110110000',
            (7, 6): '1111111110110001',
            (7, 7): '1111111110110010',
            (7, 8): '1111111110110011',
            (7, 9): '1111111110110100',
            (7, 10): '1111111110110101',
            (8, 1): '111111000',
            (8, 2): '111111111000000',
            (8, 3): '1111111110110110',
            (8, 4): '1111111110110111',
            (8, 5): '1111111110111000',
            (8, 6): '1111111110111001',
            (8, 7): '1111111110111010',
            (8, 8): '1111111110111011',
            (8, 9): '1111111110111100',
            (8, 10): '1111111110111101',
            (9, 1): '111111001',
            (9, 2): '1111111110111110',
            (9, 3): '1111111110111111',
            (9, 4): '1111111111000000',
            (9, 5): '1111111111000001',
            (9, 6): '1111111111000010',
            (9, 7): '1111111111000011',
            (9, 8): '1111111111000100',
            (9, 9): '1111111111000101',
            (9, 10): '1111111111000110',
            (10, 1): '111111010',
            (10, 2): '1111111111000111',
            (10, 3): '1111111111001000',
            (10, 4): '1111111111001001',
            (10, 5): '1111111111001010',
            (10, 6): '1111111111001011',
            (10, 7): '1111111111001100',
            (10, 8): '1111111111001101',
            (10, 9): '1111111111001110',
            (10, 10): '1111111111001111',
            (11, 1): '1111111001',
            (11, 2): '1111111111010000',
            (11, 3): '1111111111010001',
            (11, 4): '1111111111010010',
            (11, 5): '1111111111010011',
            (11, 6): '1111111111010100',
            (11, 7): '1111111111010101',
            (11, 8): '1111111111010110',
            (11, 9): '1111111111010111',
            (11, 10): '1111111111011000',
            (12, 1): '1111111010',
            (12, 2): '1111111111011001',
            (12, 3): '1111111111011010',
            (12, 4): '1111111111011011',
            (12, 5): '1111111111011100',
            (12, 6): '1111111111011101',
            (12, 7): '1111111111011110',
            (12, 8): '1111111111011111',
            (12, 9): '1111111111100000',
            (12, 10): '1111111111100001',
            (13, 1): '11111111000',
            (13, 2): '1111111111100010',
            (13, 3): '1111111111100011',
            (13, 4): '1111111111100100',
            (13, 5): '1111111111100101',
            (13, 6): '1111111111100110',
            (13, 7): '1111111111100111',
            (13, 8): '1111111111101000',
            (13, 9): '1111111111101001',
            (13, 10): '1111111111101010',
            (14, 1): '1111111111101011',
            (14, 2): '1111111111101100',
            (14, 3): '1111111111101101',
            (14, 4): '1111111111101110',
            (14, 5): '1111111111101111',
            (14, 6): '1111111111110000',
            (14, 7): '1111111111110001',
            (14, 8): '1111111111110010',
            (14, 9): '1111111111110011',
            (14, 10): '1111111111110100',
            (15, 0): '11111111001',    # ZRL
            (15, 1): '1111111111110101',
            (15, 2): '1111111111110110',
            (15, 3): '1111111111110111',
            (15, 4): '1111111111111000',
            (15, 5): '1111111111111001',
            (15, 6): '1111111111111010',
            (15, 7): '1111111111111011',
            (15, 8): '1111111111111100',
            (15, 9): '1111111111111101',
            (15, 10): '1111111111111110'
        }

    def encode_dc(self, dc_diff):
        """Encode DC coefficient difference"""
        if dc_diff == 0:
            return self.dc_table[0]
        
        # Calculate category (size)
        category = int(np.floor(np.log2(abs(dc_diff)))) + 1
        
        # Get Huffman code for the category
        huffman_code = self.dc_table[category]
        
        # Generate amplitude code
        value = int(dc_diff)
        if value < 0:
            value = abs(value)
            value = (1 << category) - value - 1
        
        amplitude = format(value, f'0{category}b')
            
        return huffman_code + amplitude

    def encode_ac(self, run_length, value):
        """Encode AC coefficient"""
        value = int(value)  # Convert float to int
        if value == 0:
            if run_length == 15:
                return self.ac_table[(15,0)]  # ZRL
            elif run_length == 0:
                return self.ac_table[(0,0)]  # EOB
            return None

        size = int(np.floor(np.log2(abs(value)))) + 1
        if (run_length, size) in self.ac_table:
            huffman_code = self.ac_table[(run_length, size)]
            
            # Generate amplitude code similar to DC
            if value < 0:
                value = abs(value)
                value = (1 << size) - value - 1
            
            amplitude = format(value, f'0{size}b')

            if len(amplitude) != size:
                print(run_length, size, value, huffman_code, amplitude)
                raise ValueError("Invalid AC amplitude code")
            
            return huffman_code + amplitude
        return None
    
class JPEGCodec:
    def __init__(self):
        self.dct = DCTTransform()
        self.huffman = HuffmanCoding()
        
        # Standard quantization table
        self.quantization_table = np.array([
            [16, 11, 10, 16, 24, 40, 51, 61],
            [12, 12, 14, 19, 26, 58, 60, 55],
            [14, 13, 16, 24, 40, 57, 69, 56],
            [14, 17, 22, 29, 51, 87, 80, 62],
            [18, 22, 37, 56, 68, 109, 103, 77],
            [24, 35, 55, 64, 81, 104, 113, 92],
            [49, 64, 78, 87, 103, 121, 120, 101],
            [72, 92, 95, 98, 112, 100, 103, 99]
        ])
        self.quantization_table = self.quantization_table / 10 # Scale down for smaller values

    def zigzag_scan(self, block):
        """Perform zigzag scanning of the block"""
        # Implementation of zigzag scanning pattern
        if block.shape != (8, 8):
            raise ValueError("Input block must be 8x8")
        
        # Zigzag pattern indices
        zigzag_pattern = [
            (0,0), (0,1), (1,0), (2,0), (1,1), (0,2), (0,3), (1,2),
            (2,1), (3,0), (4,0), (3,1), (2,2), (1,3), (0,4), (0,5),
            (1,4), (2,3), (3,2), (4,1), (5,0), (6,0), (5,1), (4,2),
            (3,3), (2,4), (1,5), (0,6), (0,7), (1,6), (2,5), (3,4),
            (4,3), (5,2), (6,1), (7,0), (7,1), (6,2), (5,3), (4,4),
            (3,5), (2,6), (1,7), (2,7), (3,6), (4,5), (5,4), (6,3),
            (7,2), (7,3), (6,4), (5,5), (4,6), (3,7), (4,7), (5,6),
            (6,5), (7,4), (7,5), (6,6), (5,7), (6,7), (7,6), (7,7)
        ]
        
        zigzag = np.zeros(64)
        for i, (row, col) in enumerate(zigzag_pattern):
            zigzag[i] = block[row, col]
        
        return zigzag

    
    def zigzag_to_block(self, zigzag_coefficients):
        """Convert zigzag sequence back to 8x8 block"""
        block = np.zeros((8, 8))
        
        # Zigzag pattern indices
        zigzag_pattern = [
            (0,0), (0,1), (1,0), (2,0), (1,1), (0,2), (0,3), (1,2),
            (2,1), (3,0), (4,0), (3,1), (2,2), (1,3), (0,4), (0,5),
            (1,4), (2,3), (3,2), (4,1), (5,0), (6,0), (5,1), (4,2),
            (3,3), (2,4), (1,5), (0,6), (0,7), (1,6), (2,5), (3,4),
            (4,3), (5,2), (6,1), (7,0), (7,1), (6,2), (5,3), (4,4),
            (3,5), (2,6), (1,7), (2,7), (3,6), (4,5), (5,4), (6,3),
            (7,2), (7,3), (6,4), (5,5), (4,6), (3,7), (4,7), (5,6),
            (6,5), (7,4), (7,5), (6,6), (5,7), (6,7), (7,6), (7,7)
        ]
        
        # Place each coefficient in its position according to zigzag pattern
        for i, (row, col) in enumerate(zigzag_pattern):
            if i < len(zigzag_coefficients):
                block[row, col] = zigzag_coefficients[i]
        
        return block

    def encode_block(self, block, prev_dc=0):
        """Encode a single 8x8 block"""
        # Level shift (subtract 128)
        shifted_block = block - 128
        
        # Forward DCT
        dct_block = self.dct.forward_dct_2d(shifted_block)
        
        # Quantization
        tmp = dct_block / self.quantization_table
        '''quantized = np.where(tmp < 0, 
                            np.round(tmp - 0.5),
                            np.where(tmp > 0,
                                    np.round(tmp + 0.5),
                                    tmp))'''
        quantized = tmp.astype(int)
        
        # Zigzag scan
        zz_sequence = self.zigzag_scan(quantized)
        
        # Entropy coding
        # Encode DC coefficient
        dc_diff = int(zz_sequence[0] - prev_dc)
        dc_code = self.huffman.encode_dc(dc_diff)
        
        # Encode AC coefficients
        ac_codes = []
        run_length = 0
        
        for ac_val in zz_sequence[1:]:
            if ac_val == 0:
                run_length += 1
                if run_length == 16:
                    ac_codes.append(self.huffman.encode_ac(15, 0))
                    run_length = 0
            else:
                # Encode run_length/size
                ac_code = self.huffman.encode_ac(run_length, ac_val)
                if ac_code:
                    ac_codes.append(ac_code)
                run_length = 0
        
        # Add EOB if needed
        if run_length > 0:
            ac_codes.append(self.huffman.encode_ac(0, 0))  # EOB

        return dc_code, ac_codes, zz_sequence[0]

    def decode_block(self, dc_code, ac_codes, prev_dc):
        """Decode a single 8x8 block"""
        # Initialize 64 coefficients (8x8 block in zigzag order)
        coefficients = np.zeros(64)
        
        # Decode DC coefficient
        # First find the category from dc_code using DC Huffman table
        dc_category = None
        for category, code in self.huffman.dc_table.items():
            if dc_code[:len(dc_code)-category] == code:
                dc_category = category
                amplitude_bits = dc_code[len(code):]
                break

        if dc_category is None:
            raise ValueError("Invalid DC Huffman code")
        
        if dc_category is not None:
            if dc_category == 0:
                coefficients[0] = prev_dc
            else:
                if len(amplitude_bits) != dc_category:
                    raise ValueError("Invalid DC amplitude bits length")
                # Convert amplitude_bits to value
                value = int(amplitude_bits, 2)
                
                if amplitude_bits[0] == '0': # If the first bit is 0, it's a negative value
                    value = -(1 << dc_category) + value + 1

                coefficients[0] = prev_dc + value
        
        # Decode AC coefficients
        current_position = 1
        for ac_code in ac_codes:
            if ac_code == self.huffman.ac_table[(0,0)]:  # EOB
                break
            if ac_code == self.huffman.ac_table[(15,0)]:  # ZRL
                current_position += 16
                continue
                
            # Find run_length/size combination from AC Huffman table
            for (run_length, size), code in self.huffman.ac_table.items():
                if ac_code[:len(ac_code) - size] == code:
                    current_position += run_length
                    if current_position >= 64:  # Bounds check
                        raise ValueError("Position exceeds block size")
                    
                    amplitude_bits = ac_code[len(code):]
                    if len(amplitude_bits) != size:
                        raise ValueError("Invalid AC amplitude bits length")
                    # Standard JPEG method for negative values
                    value = int(amplitude_bits, 2)
                    if amplitude_bits[0] == '0': # If the first bit is 0, it's a negative value
                        value = -(1 << size) + value + 1
                        
                    coefficients[current_position] = value
                    current_position += 1
                    break
        
        # Reverse zigzag scan
        block = self.zigzag_to_block(coefficients)

        # Dequantize
        dequantized = block * self.quantization_table

        # Inverse DCT
        idct_block = self.dct.inverse_dct_2d(dequantized)
        
        # Level shift (add 128)
        return idct_block + 128, coefficients[0]

def main():
    # Read the image file and convert to grayscale
    img = plt.imread('lady.jpg')
    if len(img.shape) == 3:  # Convert color image to grayscale
        test_image = np.mean(img, axis=2).astype(np.uint8)
    else:
        test_image = img
    
    # Get image dimensions
    height, width = test_image.shape
    
    # Pad image if dimensions are not multiples of 8
    pad_height = (8 - height % 8) if height % 8 != 0 else 0
    pad_width = (8 - width % 8) if width % 8 != 0 else 0
    
    if pad_height > 0 or pad_width > 0:
        test_image = np.pad(test_image, ((0, pad_height), (0, pad_width)), 'edge')
    
    # Initialize codec
    codec = JPEGCodec()
    
    # Encode image block by block
    encoded_data = []
    prev_dc = 0
    compressed_size = 0
    
    for i in range(0, height, 8):
        for j in range(0, width, 8):
            block = test_image[i:i+8, j:j+8]
            dc_code, ac_codes, new_dc = codec.encode_block(block, prev_dc)
            encoded_data.append((dc_code, ac_codes))
            
            # Calculate compressed size in bits
            compressed_size += len(dc_code)
            compressed_size += sum(len(code) for code in ac_codes)
            
            prev_dc = new_dc
    
    # Decode image
    decoded_image = np.zeros_like(test_image)
    block_idx = 0
    prev_dc = 0
    
    for i in range(0, height, 8):
        for j in range(0, width, 8):
            dc_code, ac_codes = encoded_data[block_idx]
            decoded_block, new_dc = codec.decode_block(dc_code, ac_codes, prev_dc)
            decoded_image[i:i+8, j:j+8] = decoded_block
            
            # Update prev_dc for next block
            prev_dc = new_dc  # DC coefficient
            block_idx += 1

    # Calculate compression ratio
    original_size = test_image.size * 8  # 8 bits per pixel
    compression_ratio = original_size / compressed_size
    
    # Calculate PSNR
    mse = np.mean((test_image - decoded_image) ** 2)
    max_pixel = 255
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    
    # Display results
    plt.figure(figsize=(15, 5))
    
    plt.subplot(131)
    plt.imshow(test_image, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(132)
    plt.imshow(decoded_image, cmap='gray')
    plt.title('Reconstructed Image')
    plt.axis('off')
    
    plt.subplot(133)
    plt.imshow(np.abs(test_image - decoded_image), cmap='hot')
    plt.title('Error Map')
    plt.colorbar()
    plt.axis('off')
    
    plt.suptitle(f'Compression Ratio: {compression_ratio:.2f}\nPSNR: {psnr:.2f} dB')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()