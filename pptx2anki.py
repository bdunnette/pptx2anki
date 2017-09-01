#!/usr/bin/env python3

import sys, os
import genanki
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

my_model = genanki.Model(
  1234567890,
  'Simple Model',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
  ])

deck_name = os.path.splitext(os.path.basename(sys.argv[1]))[0]

my_deck = genanki.Deck(
  1234567890,
  deck_name)

my_package = genanki.Package(my_deck)
my_package.media_files = []

prs = Presentation(sys.argv[1])
print(prs)
print(len(prs.slides))
slide_info = [dict() for i in range(len(prs.slides))]
for slide_index, slide in enumerate(prs.slides):
    # print("\n\n")
    # print(slide_index)
    # print(prs.slides[slide_index+1])
    # print(slide)
    # print(slide.notes_slide)
    note_text = ""
    for ns in slide.notes_slide.shapes:
        if not str(ns.text).isnumeric():
            note_text += str(ns.text)
    # print(note_text)
    slide_info[slide_index]['text'] = note_text.strip()
    # print(slide.shapes)
    for shape in slide.shapes:
        # print(shape)
        # print(shape.shape_type)
        if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
            # print(shape.image)
            # print(shape.image.filename)
            # print(shape.image.size)
            # print(shape.image.ext)
            # print(shape.image.content_type)
            # print(shape.image.blob)
            image_file = "%s.%s" % (slide_index, shape.image.ext)
            with open(image_file, 'wb') as f:
                f.write(shape.image.blob)
            slide_info[slide_index]['image'] = image_file

# print(slide_info)
for idx, slide in enumerate(slide_info):
    if 'image' in slide and not 'processed' in slide:
        print(slide)
        next_slide = slide_info[idx+1]
        print(slide['text'] == next_slide['text'])
        print(slide['text'])
        if slide['text'] == next_slide['text']:
            back_text = "<img src='%s'><p>%s</p>" % (next_slide['image'],slide['text'])
            my_package.media_files.append(next_slide['image'])
            slide_info[idx+1]['processed'] = True
        else:
            back_text = slide['text']
        my_note = genanki.Note(
          model=my_model,
          sort_field=idx,
          fields=["<img src='%s'>" % slide['image'],back_text])
        my_deck.add_note(my_note)
        my_package.media_files.append(slide['image'])

my_package.write_to_file('%s.apkg' % deck_name)
