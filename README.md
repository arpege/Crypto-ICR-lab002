# Crypto ICR - lab002

Create an utility that could create and read medical's containers for sensible informations. The containers are scheduled for archiving. They should not pass sensitive information without the encryption keys.

## Requirements

1. We must be able to detect that the archive was changed after generation
2. We must guarantee its integrity
3. We must guarantee its provenance
4. The meta data should not help to retrieve sensitive information

## Medivac

Medivac is the name of the utility created to meet the criteria of the labo. It is a scrypt python that encapsulates several sensitive files in a single encrypted container.

### Usage
**To encrypt several files**

`./medivac file1.txt file2.txt [file path]`

Scrypt output :

```
./medivac file1.txt file2.txt
  __  __          _ _                 
 |  \/  |        | (_)                
 | \  / | ___  __| |___   ____ _  ___ 
 | |\/| |/ _ \/ _` | \ \ / / _` |/ __|
 | |  | |  __/ (_| | |\ V / (_| | (__ 
 |_|  |_|\___|\__,_|_| \_/ \__,_|\___|
  ___                       _   
 | __|_ _  __ _ _ _  _ _ __| |_ 
 | _|| ' \/ _| '_| || | '_ \  _|
 |___|_||_\__|_|  \_, | .__/\__|
                  |__/|_|       
                  
                  

  Start compresion...

   * Adding file1.txt
   * Adding file2.txt


  Start encryption...

bytearray(b"PK\x03\x04\x14\x00\x00\x00\x00\x00\xa6v...\x00")

  Removing temp files...

   * medfile.zip removed

   ----------------------------------------
  | Medivac encryption finish with success |
   ----------------------------------------
  

```


**To encrypt a medivac file**

`./medivac -d [file] [path dir]` i.e: `./medivac -d medfile.medivac ./out/`

Scrypt output :

```
./medivac -d medfile.medivac ./out/
  __  __          _ _                 
 |  \/  |        | (_)                
 | \  / | ___  __| |___   ____ _  ___ 
 | |\/| |/ _ \/ _` | \ \ / / _` |/ __|
 | |  | |  __/ (_| | |\ V / (_| | (__ 
 |_|  |_|\___|\__,_|_| \_/ \__,_|\___|
  ___                       _   
 |   \ ___ __ _ _ _  _ _ __| |_ 
 | |) / -_) _| '_| || | '_ \  _|
 |___/\___\__|_|  \_, | .__/\__|
                  |__/|_|       
                  
                  
  Reading file medfile.medivac
  Output result in ./out/

bytearray(b"PK\x03\x04...\x00")

  Removing temp files...

   * medfile.zip removed

   ----------------------------------------
  | Medivac decryption finish with success |
   ----------------------------------------
  

```

### Installation

To test it on a UNIX environment you can execute `make install`. It will effectively copy the executable in the folder `/usr/local/bin`.