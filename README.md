# Crypto ICR - lab002

Create an utility that could create and read medical's containers for sensible informations. The containers are scheduled for archiving. They should not pass sensitive information without the encryption keys.

## Medivac

Medivac is the name of the utility created to meet the criteria of the labo. It is a scrypt python that encapsulates several sensitive files in a single encrypted container.

### Usage
**To encrypt several files**

`./medivac file1.txt file2.txt [file path]`

Scrypt output :

```bash
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

bytearray(b"PK\x03\x04\x14\x00\x00\x00\x00\x00\xa6v\xa5H\x16\xe5\'|\x0f\x00\x00\x00\x0f\x00\x00\x00\t\x00\x00\x00file1.txtsercet med filePK\x03\x04\x14\x00\x00\x00\x00\x00\xa6v\xa5H\x94P/\x80\x16\x00\x00\x00\x16\x00\x00\x00\t\x00\x00\x00file2.txtsecond secret med filePK\x01\x02\x14\x03\x14\x00\x00\x00\x00\x00\xa6v\xa5H\x16\xe5\'|\x0f\x00\x00\x00\x0f\x00\x00\x00\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa4\x81\x00\x00\x00\x00file1.txtPK\x01\x02\x14\x03\x14\x00\x00\x00\x00\x00\xa6v\xa5H\x94P/\x80\x16\x00\x00\x00\x16\x00\x00\x00\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa4\x816\x00\x00\x00file2.txtPK\x05\x06\x00\x00\x00\x00\x02\x00\x02\x00n\x00\x00\x00s\x00\x00\x00\x00\x00")

  Removing temp files...

   * medfile.zip removed

   ----------------------------------------
  | Medivac encryption finish with success |
   ----------------------------------------
  

```
