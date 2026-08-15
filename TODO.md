# Until the site is finished

Everything left before `hannes-meilicke.com` can come out of holding mode.
Your items are marked **(you)** — they need your words, your files or your
judgement, and I cannot do them for you. Mine are marked **(me)** — say the
word and they are done.

Three a day. The order in [Suggested order](#suggested-order) is chosen so
nothing waits on something you have not done yet.

---

## 1. Writing — the words that are still placeholders

`tools/check.py` counts **301 unfinished passages**. Almost all of them are
here. The number went up by 61 when the year pages were rebuilt: every
honorable mention now has a back face waiting for a description, so work that
was invisible before is now counted.

- [ ] **(you)** Write **About me** — the section under the hero.
- [ ] **(you)** Write **In the clinic** — the lead sentence and the three
      short pieces (Clinical psychiatry / Psychotherapy / Time with patients).
- [ ] **(you)** Write **Away from the desk** — one short line in each of the
      four boxes (football, exercising, language learning, reading).
- [ ] **(you)** Write **Research & Publications** — the section description.
- [ ] **(you)** Write **Research & Publications** — a description for each of
      the three boxes.
- [ ] **(you)** Write **How 20XX read** — one note for each of the eight years
      (2018–2025). Two or three sentences each.
- [ ] **(you)** Write **What I learned** — for each of the 27 intellectual
      heroes. This is the longest single item on the list; consider splitting
      it across several days rather than counting it as one.
- [ ] **(you)** Write **descriptions for the honorable mentions** — the flip
      side of each cover. One or two lines each.
- [ ] **(you)** Write **What this one changed** for the ranked books — ten a
      year, eight years. Also worth splitting.
- [ ] **(you)** Write one real **media piece** and one **video** entry, to
      replace the four `example-*.html` templates.
- [ ] **(you)** Fill in the real **publications** list.

## 2. Facts still marked XXX

- [ ] **(you)** **Research fellowship, XXX** — the institution name.
- [ ] **(you)** **US clinical experience** — the two `University of XXX` lines.
- [ ] **(you)** Hero affiliation line — `Department of Psychiatry and
      Psychology, XXX`.
- [ ] **(you)** Doctorate **thesis title** — currently *"placeholder"*.

## 3. Files you need to supply

- [ ] **(you)** **cv.pdf** — two buttons link to it and it does not exist.
      This is the site's only dead link.
- [ ] **(you)** **photo.jpg** — the hero portrait. The block hides itself
      while the file is missing, so the hero currently has no picture.
- [ ] **(you)** Pictures for **Research fellowship**, **US clinical
      experience** and **Medical studies** — the empty photo slots in the CV.
- [ ] **(you)** **Heilbronn, Germany** — review the five childhood pictures and
      decide which to keep.
- [ ] **(you)** **og.jpg** — the 1200×630 image shown when the site is shared
      on WhatsApp, LinkedIn or Slack. Referenced by every page; missing.

## 4. Design decisions waiting on you

- [ ] **(you)** **Hero font** — you do not like the current one. I will put
      five or six side by side in the real headline for you to pick from.
- [ ] **(you)** **Top-left name treatment** — the mosaic strip. Keep it, tune
      it, or go back to the letterspaced type.
- [ ] **(you)** **Hero monogram mosaic** — ten panels were generated and you
      have not picked one; the hero is unchanged. Decide or discard.

## 5. Credits and legal

- [ ] **(you + me)** **A credits page.** You asked for this to be given
      "in a separate way somewhere". Right now the picture credits are a
      paragraph inside the Impressum. I would make `/credits.html`, linked
      from the footer, listing: book jackets (publishers), the 27 portraits
      (photographers, and the right to one's own image for the living), the
      childhood covers (Nintendo, Game Freak, Paws Inc., 20th Television),
      the AI-generated hobby tiles, and the three fonts. You tell me what you
      want said; I build it.
- [ ] **(me)** Replace portraits whose licence is unclear with ones that are
      clearly free, or drop them. Several of the 27 are ordinary press photos.
- [ ] **(you)** Decide whether Impressum and Datenschutz stay German-only.
      My recommendation: yes — they are German legal documents and a
      translation invites the question of which version governs.

## 6. Housekeeping I can do without you

- [ ] **(me)** Compress the five images over 400 KB. `shanghai6.jpeg` alone is
      3.5 MB, which is larger than the rest of the site put together.
- [ ] **(me)** Delete the 15 unused images still in the repository.
- [ ] **(me)** Alt text on every meaningful image — decorative ones are
      correctly empty, but the CV and childhood photographs should describe
      themselves.
- [ ] **(me)** A `sitemap.xml` and a `robots.txt` that match it.
- [ ] **(me)** Remove the `noindex` tags. Seventeen pages carry one, which is
      right while the site is hidden and wrong the day it opens.

## 7. Launch day

Do these in order, on the same day, once everything above is done.

- [ ] **(me)** Run `python3 tools/relaunch.py` — undoes holding-page mode and
      puts the real site back at `/`.
- [ ] **(me)** Final pass of `tools/check.py`; nothing unfinished, no dead
      links.
- [ ] **(you)** Activate the **FormSubmit** address so the contact form
      actually delivers. Needs one confirmation e-mail from you.
- [ ] **(you)** Add the site URL to your four profiles — Google Scholar,
      ORCID, ResearchGate, LinkedIn.
- [ ] **(you)** Register the site in **Google Search Console** and submit the
      sitemap.
- [ ] **(you)** Open it on your own iPhone and iPad and read it end to end.

---

## Suggested order

Three a day. Writing first, because it is the long pole and everything else
is quick by comparison.

| Day | Three things |
|-----|--------------|
| 1 | About me · In the clinic · Away from the desk (4 lines) |
| 2 | The three XXX facts · thesis title · cv.pdf |
| 3 | Research & Publications description · the three box descriptions · photo.jpg |
| 4 | How 2018 read · How 2019 read · How 2020 read |
| 5 | How 2021 read · How 2022 read · How 2023 read |
| 6 | How 2024 read · How 2025 read · og.jpg |
| 7 | Hero font choice · name treatment · mosaic panel |
| 8 | Heroes 1–9: what I learned |
| 9 | Heroes 10–18 |
| 10 | Heroes 19–27 |
| 11 | Honorable mentions 2018 · 2019 · 2020 |
| 12 | Honorable mentions 2021 · 2022 · 2023 |
| 13 | Honorable mentions 2024 · 2025 · CV pictures |
| 14 | Ranked books 2018 · 2019 · Heilbronn picture review |
| 15 | Ranked books 2020 · 2021 · 2022 |
| 16 | Ranked books 2023 · 2024 · 2025 |
| 17 | One media piece · one video · publications list |
| 18 | Credits page (tell me what to say) · legal decision · my housekeeping |
| 19 | Launch day |

---

## Done

- Light theme rebuilt and measured for contrast
- Dark as the default
- Year emblems centred on their numerals
- Childhood gallery, birth – 2017
- Book pairs split; every jacket found and checked by eye
- Two-book cards lean rather than stack
- 15–11 shows all five, every year
- Mobile: buttons in one row, CV photos three over two, heroes ranked, the
  portrait handed over by scrolling
- The nav row could not be scrolled back to Home on a phone; fixed
- Private-key guard in the pre-commit hook
- Font payload 212 KB → 2.7 KB
