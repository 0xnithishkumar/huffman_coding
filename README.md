# Huffman Coding
This code implements Huffman coding, a lossless data compression algorithm. Huffman coding assigns variable-length codes to characters based on their frequencies in the input text, with more frequent characters getting shorter codes.


## Usage
* To compress a file:
  * Provide the path to the file you want to compress as the input.
  * The program will perform Huffman coding and generate a compressed binary file (with the extension .bin).
  * Additionally, a key file (with the extension _key.bin) will be generated, containing the mapping of characters to their corresponding Huffman codes.

* To decompress a file:
  * Provide the path to the compressed binary file (with the extension .bin) as the input.
  * The program will use the key file to decode the compressed binary file and generate the original file.

* File extensions:
  * Input file: test.txt
  * Compressed file: test.bin
  * Key file for decompression: test_key.bin
  * Decompressed output file: test_decompressed.txt


## Code Explanation
The code consists of the following classes and methods:

### Binary_tree class
* `__init__(self, value, frequency, left=None, right=None)`: Initializes a binary tree node with a value, frequency, and optional left and right child nodes.
* `__lt__(self, other)`: Overloads the < operator to compare nodes based on their frequencies.
* `__eq__(self, other)`: Overloads the == operator to compare nodes based on their frequencies.

### Huffman_code class
* `__init__(self, path)`: Initializes the Huffman code object with a file path.
* `__frequency_from_text(self, text)`: Generates a frequency dictionary for characters in the given text.
* `__build_heap(self, frequency_dict)`: Builds a minimum heap from the frequency dictionary.
* `__build_binary_tree(self)`: Builds a binary tree using the minimum heap.
* `__build_tree_code_helper(self, root, bit)`: Recursively builds a code dictionary by traversing the binary tree.
* `__build_tree_code(self, topnode)`: Builds a code dictionary using the top node of the binary tree.
* `__build_encoded_test(self, text)`: Encodes the input text using the code dictionary.code class
* `__build_padded_encoded_text(self, encoded_text)`: Pads the encoded text and adds padding information at the beginning.
* `__build_padded_array(self, padded_encoded_text)`: Converts the padded encoded text into a byte representation.
* `__build_code_to_bytes(self)`: Converts the code dictionary into a byte object.
* `compress(self)`: Compresses the file using Huffman coding and generates a compressed binary file and a key file.
* `__build_generate_code(self, key_file_name, key_file_extension)`: Generates a code dictionary from the key file.
* `__remove_padding(self, bit_string)`: Removes padding value and padding info from the bit string.
* `__decoded_text(self, unpadded_string, dict_code)`: Decodes the unpadded string using the code dictionary.
* `decompress(self, input_path)`: Decompresses the compressed binary file using the key file and generates the original file.


## Main
The main part of the code prompts the user for the file path, creates an instance of the Huffmancode class, and calls the compress and decompress methods to perform compression and decompression, respectively. The compressed and decompressed files are saved with appropriate file extensions.

Please make sure to have the required libraries installed before running the code: heapq, os, and pickle.

Note: The code assumes that the input file is in text format.
