export default function Patients() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Patient Directory</h2>
          <p className="text-textMuted mt-1">Manage hospital patients and records.</p>
        </div>
        <button className="btn-primary">Add Patient</button>
      </div>
      
      <div className="glass-panel overflow-hidden">
        <table className="w-full text-left text-sm text-textMuted">
          <thead className="text-xs text-white uppercase bg-black/40 border-b border-white/10">
            <tr>
              <th className="px-6 py-4">ID</th>
              <th className="px-6 py-4">Name</th>
              <th className="px-6 py-4">Status</th>
              <th className="px-6 py-4">Agent Assigned</th>
              <th className="px-6 py-4">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr className="border-b border-white/5 hover:bg-white/5 transition-colors">
              <td className="px-6 py-4 font-medium text-white">#8492</td>
              <td className="px-6 py-4">John Doe</td>
              <td className="px-6 py-4"><span className="px-2 py-1 bg-emerald-400/10 text-emerald-400 rounded-md text-xs font-medium">In Treatment</span></td>
              <td className="px-6 py-4">Treatment Planning</td>
              <td className="px-6 py-4"><button className="text-primary hover:underline">View Record</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
