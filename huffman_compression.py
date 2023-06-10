# # # Libraries
import heapq, os, pickle

# # Binary_tree class 
class Binary_tree:
    def __init__(self, value, frequency, left = None, right = None) -> None:
        self.value = value
        self.frequency = frequency
        self.left = None
        self.right = None
# Overloading '<' and '==' to use in creation of binary tree from minimum heap
    def __lt__(self, other):
        return self.frequency < other.frequency
    
    def __eq__(self, other):
        return self.frequency == other.frequency

# # Huffmancode class
class Huffmancode:
    # consists heap and code
    def __init__(self, path):
        self.path = path
        self.__heap = []
        self.__code = dict()
    
    # To generate frequency of chars from text
    def __frequency_from_text(self, text):
        frequency_dict = dict()
        for key in text:
            if key not in frequency_dict: frequency_dict[key] = 1
            else: frequency_dict[key] += 1
        return frequency_dict
    
    # To build heap from the frequency
    def __build_heap(self, frequency_dict):
        # building heap with chars in heap
        for key in frequency_dict:
            frequency_node_value = frequency_dict[key]
            # Creating binary tree nide with key and value, i.e., character and frequency
            binary_node = Binary_tree(key, frequency_node_value)
            # Creating minimum heap
            heapq.heappush(self.__heap, binary_node)
    
    # To build binary tree using minimum heap
    def __build_binary_tree(self):
        # Until there is only 1 node in heap
        while len(self.__heap)>1:
            bt_node1 = heapq.heappop(self.__heap)
            bt_node2 = heapq.heappop(self.__heap)
            # Creating new node which has frequency sum of node1 and node2
            sum_node3 = bt_node1.frequency + bt_node2.frequency
            # Creating new binary tree node with value as None
            new_node = Binary_tree(value= None, frequency= sum_node3)
            # Pushing new node into minimum heap
            heapq.heappush(self.__heap, new_node)
            # Linking node1 and node2 to the new sum node in binary tree 
            new_node.left = bt_node1
            new_node.right = bt_node2
        # Returning top node
        top_node = heapq.heappop(self.__heap)
        return top_node
    
    # To generate the code dictionary 
    def __build_tree_code_helper(self, root, bit):
        # If value is not none, i.e., if root has a character as a value (Only leaf node has values as return)
        if root.value is not None: self.__code[root.value] = bit; return
        # Adding 0 or 1 for left and right nodes respectively
        self.__build_tree_code_helper(root.left, bit+'0')
        self.__build_tree_code_helper(root.right, bit+'1')

    # To build code dictionary
    def __build_tree_code(self, topnode):
        self.__build_tree_code_helper(topnode, '')
    
    # To encode the text
    def __build_encoded_test(self, text):
        encoded_text = ''
        # Encoding each character in text with code dictionary
        for i in text: encoded_text += self.__code[i]
        return encoded_text
    
    # Pad the encoded text 
    def __build_padded_encoded_text(self, encoded_text):
        # Getting the number of bits need to be encoded
        padding_value = 8 - (len(encoded_text)%8)
        # Adding the bits to the end of the encoded_text
        for i in range(padding_value): encoded_text += '0'
        # Add number of bits added to the start of the encoded text
        padded_info = format(padding_value,'08b')
        return padded_info + encoded_text
    
    # To create byte representation of the padded_encoded_text
    def __build_padded_array(self, padded_encoded_text):
        array = []
        # Dividing padded_encoded_text into chucks of 8
        for i in range(0, len(padded_encoded_text), 8):
            chucks = padded_encoded_text[i:i+8]
            # Creating integer equivalent of text binary and appending it to array
            array.append(int(chucks, 2))
        # Converting array of integers into byte object
        final_byte = bytes(array)
        return final_byte
    
    # To convert dictionarty into bytes
    def __build_code_to_bytes(self):
        byte_object = pickle.dumps(self.__code)
        return byte_object
    
    # Compression function
    def compress(self):
        # extract text from file
        file_name, file_extension = os.path.splitext(self.path)
        output_path = f"{file_name}.bin"
        key_path = f"{file_name}_key.bin"
        # Opening path in read and write mode and output_path in write binary mode  
        with open(self.path, 'r+') as file, open(output_path, 'wb') as output, open(key_path, 'wb') as key_output:
            text = file.read()
            text = text.rstrip(' ')
            # create frequency dictionary using _frequency_from_text
            frequency_dict = self.__frequency_from_text(text)
            # create minimum heap for frequency 
            self.__build_heap(frequency_dict)
            # construcy binary tree from minimum heap
            top_node = self.__build_binary_tree()
            # create new dictionary for codes
            self.__build_tree_code(top_node)
            # encode the bits with frequency dictionary
            encoded_text = self.__build_encoded_test(text)
            # padding of encoded text
            padded_encoded_text = self.__build_padded_encoded_text(encoded_text)
            # return the binray file
            final_bytes = (self.__build_padded_array(padded_encoded_text))
            # Writing into output file
            output.write(final_bytes)
            # Convert code dictionary into .txt
            code_byte_object = self.__build_code_to_bytes()
            # write bin into key_output
            key_output.write(code_byte_object)
        return output_path, key_path
    
    # To convert bytes dictionary into dictionary code using which we decompress
    def __build_generate_code(self, key_file_name, key_file_extension):
        with open(key_file_name + key_file_extension, 'rb') as f:
            dict_code = pickle.loads(f.read())
        return dict_code
    
    # Remove padding value and padding info
    def __remove_padding(self, bit_string):
        pad_value = int(bit_string[:8], 2)
        unpadded_string = bit_string[8:-pad_value]
        return unpadded_string
    
    # decode each char using code dictionary
    def __decoded_text(self, upadded_string, dict_code):
        reversed_code = dict(zip(list(dict_code.values()), list(dict_code.keys())))
        cur_bit = ''
        actual_text = ''
        for i in upadded_string:
            cur_bit += i
            if cur_bit in reversed_code: 
                actual_text += reversed_code[cur_bit]
                cur_bit = ''
        return actual_text
            
    # Decompress function
    def decompress(self, input_path):
        file_name, file_extension = os.path.splitext(input_path)
        key_file_name, key_file_extension = f"{file_name}_key" , ".bin"
        output_path = file_name + '_decompressed' +'.txt'
        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            bit_string = ''
            # Read the first byte character
            byte = file.read(1)
            while byte:
                # Converting byte character into interger
                byte = ord(byte)
                # Converting into bits
                bits = bin(byte)[2:].rjust(8, '0')
                # Add the bits into bit_string
                bit_string += bits
                byte = file.read(1) 
            unpadded_string = self.__remove_padding(bit_string)
            # create code dictionary from key.bin
            dict_code = self.__build_generate_code(key_file_name, key_file_extension)
            actual_text = self.__decoded_text(unpadded_string, dict_code)
            output.write(actual_text)
        return output_path

# --------------------Main--------------------
# Creation of object of huffman class
path = input("Enter the path of the file: ")
h = Huffmancode(path)

# Compression function
h.compress()
print("Compressed file generated")

#  Decompression function
compressed_file_name = input("Enter the path of compressed file: ")
h.decompress(compressed_file_name)
print("Decompressed file generated")