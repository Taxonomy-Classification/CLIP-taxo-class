import json

input_file = "./data/textaug_train_full_capaug.json"
output_file = "./data/textaug_train_full_capaug_compressed.json"

def safe_access_captions(captions, index):
    try:
        if captions[index].startswith("This belongs to"):
            return captions[index][14:]
        else:
            return None
    except IndexError:
        return None

def modify_captions(captions, species):
    modified_captions = []
    taxonomic_caption_count = 0
    over = 0

    # Modify caption 2
    modified_captions.append(f"'This is an image of an animal with taxon name: {species}. This is its species name. species: {species} {captions[3]}")

    taxonomic_captions = [caption for caption in captions if caption.startswith("This belongs to")]
    non_taxonomic_captions = [caption for caption in captions[4:] if not caption.startswith("This belongs to")]

    # Remove duplicate captions from non_taxonomic_captions
    non_taxonomic_captions = list(set(non_taxonomic_captions))

    # Combine taxonomic captions
    for i in range(0, len(taxonomic_captions), 3):
        combined_caption_parts = taxonomic_captions[i:i+3]
        combined_caption = f"{species} belongs to {' It also belongs to '.join([part[16:] for part in combined_caption_parts])}."
        if len(combined_caption) > 273:
            over += 1
        taxonomic_caption_count += 1
        modified_captions.append(combined_caption[:273])

    # Join non-taxonomic captions
    non_taxonomic_captions_combined = []
    current_caption = ''
    for caption in non_taxonomic_captions:
        if len(current_caption + ' ' + caption) <= 273:
            current_caption += ' ' + caption
        else:
            non_taxonomic_captions_combined.append(current_caption.strip())
            current_caption = caption
    if current_caption:
        non_taxonomic_captions_combined.append(current_caption.strip())

    # Add non-taxonomic captions
    modified_captions.extend(non_taxonomic_captions_combined)
  
    return modified_captions, over, taxonomic_caption_count


with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
    over = 0
    taxonomic_caption_count = 0
    for line in f_in:
        item = json.loads(line)
        species = item["species"]
        try:
            item['captions'], new_over, new_taxo_cap_count = modify_captions(item['captions'], species)
            over += new_over
            taxonomic_caption_count += new_taxo_cap_count
        except:
            print(f"Error with {item['filename']}")
            print(f"Captions: {item['captions']}")
        f_out.write(json.dumps(item) + '\n')
    print("total taxonomic caption count: ", taxonomic_caption_count, "overflowed (>273): ", over, "overflow percentage: ", over/taxonomic_caption_count)
