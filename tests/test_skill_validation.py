from pathlib import Path
import importlib.util
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT/'tools/validate_skill.py'


class SkillValidation(unittest.TestCase):
    def setUp(self):
        self.assertTrue(VALIDATOR.is_file(), 'Skill validator not implemented')
        spec = importlib.util.spec_from_file_location('skill_validator',VALIDATOR)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.skill = Path(self.temp.name)/'cionejr'
        self.skill.mkdir()
        self.entry = self.skill/'SKILL.md'
        self.entry.write_text('---\nname: cionejr\ndescription: Draw and review illustrations.\n---\n# cionejr\n',encoding='utf-8')

    def test_valid_minimal_skill(self):
        self.assertEqual(self.module.validate_skill(self.skill),[])

    def test_missing_entry_is_reported(self):
        self.entry.unlink()
        self.assertTrue(self.module.validate_skill(self.skill))

    def test_missing_frontmatter_is_reported(self):
        self.entry.write_text('# cionejr\n',encoding='utf-8')
        self.assertTrue(self.module.validate_skill(self.skill))

    def test_bad_yaml_is_reported_without_traceback(self):
        self.entry.write_text('---\nname: [\n---\n',encoding='utf-8')
        self.assertTrue(self.module.validate_skill(self.skill))

    def test_frontmatter_must_be_mapping(self):
        self.entry.write_text('---\n- cionejr\n---\n',encoding='utf-8')
        self.assertTrue(self.module.validate_skill(self.skill))

    def test_name_must_match_directory(self):
        self.entry.write_text('---\nname: other\ndescription: Draw.\n---\n',encoding='utf-8')
        self.assertTrue(self.module.validate_skill(self.skill))

    def test_name_must_follow_skill_syntax(self):
        self.entry.write_text('---\nname: Bad--Name\ndescription: Draw.\n---\n',encoding='utf-8')
        self.assertTrue(self.module.validate_skill(self.skill))

    def test_description_must_be_nonempty_string(self):
        for description in ('""','false','123'):
            with self.subTest(description=description):
                self.entry.write_text(f'---\nname: cionejr\ndescription: {description}\n---\n',encoding='utf-8')
                self.assertTrue(self.module.validate_skill(self.skill))

    def test_long_description_is_rejected(self):
        self.entry.write_text('---\nname: cionejr\ndescription: '+('x'*1025)+'\n---\n',encoding='utf-8')
        self.assertTrue(self.module.validate_skill(self.skill))

    def test_missing_local_link_is_reported(self):
        with self.entry.open('a',encoding='utf-8') as file:
            file.write('[Reference](references/missing.md)\n')
        self.assertTrue(self.module.validate_skill(self.skill))

    def test_bundled_link_cannot_escape_skill(self):
        outside = self.skill.parent/'private.md'
        outside.write_text('not bundled',encoding='utf-8')
        with self.entry.open('a',encoding='utf-8') as file:
            file.write('[Outside](../private.md)\n')
        self.assertTrue(self.module.validate_skill(self.skill))

    def test_link_in_supporting_file_is_checked(self):
        reference = self.skill/'notes.md'
        reference.write_text('[Missing](no-file.md)\n',encoding='utf-8')
        self.assertTrue(self.module.validate_skill(self.skill))

    def test_https_and_existing_local_links_are_accepted(self):
        (self.skill/'notes.md').write_text('# Notes\n',encoding='utf-8')
        with self.entry.open('a',encoding='utf-8') as file:
            file.write('[Web](https://example.org/)\n[Notes](notes.md#heading)\n')
        self.assertEqual(self.module.validate_skill(self.skill),[])

    def test_windows_absolute_path_is_rejected_on_any_os(self):
        with self.entry.open('a',encoding='utf-8') as file:
            file.write('[Private](C:/Users/person/notes.md)\n')
        self.assertTrue(self.module.validate_skill(self.skill))

    def test_metadata_values_must_be_strings(self):
        self.entry.write_text('---\nname: cionejr\ndescription: Draw.\nmetadata:\n  version: 1\n---\n',encoding='utf-8')
        self.assertTrue(self.module.validate_skill(self.skill))

    def test_cli_returns_zero_for_valid_skill(self):
        result = subprocess.run([sys.executable,str(VALIDATOR),str(self.skill)],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)

    def test_cli_returns_one_for_invalid_skill(self):
        self.entry.unlink()
        result = subprocess.run([sys.executable,str(VALIDATOR),str(self.skill)],capture_output=True,text=True)
        self.assertEqual(result.returncode,1,result.stderr)


if __name__=='__main__':
    unittest.main()
