using Classes.Units;
using Methods;

namespace PeasantsAscension
{
    public class ProgramUI
    {
        public void Run()
        {
            Battle BattleManager = new Battle();
            BattleManager.BattleSystem();
        }
    }
}
